import argparse
import json
import logging
from datetime import datetime, timedelta, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold
from xgboost import XGBRegressor

from common import CATEGORIES, HERE, load_airports
from fetch_awos import load_awos

log = logging.getLogger("train")

TRAIN_DIR = HERE / "training"
MODEL_DIR = TRAIN_DIR / "models"
RESULTS = TRAIN_DIR / "results.md"
PREDICTIONS = TRAIN_DIR / "cv_predictions.csv"
BANGKOK = timezone(timedelta(hours=7))
FOLDS = 5
QM_QUANTILES = np.linspace(0, 1, 101)
CAT_BOUNDS = [upper for _, upper in CATEGORIES[:-1]]
NUMERIC = ["point_mm", "mean_r1", "max_r1", "mean_r3", "max_r3", "mean_r7", "max_r7", "wetfrac1_r7", "wetfrac10_r7",
           "lat", "lon", "doy_sin", "doy_cos"]


def load_table(run, near_only):
    feats = pd.read_csv(TRAIN_DIR / "wrfda_features.csv", dtype={"init": str}, encoding="utf-8-sig")
    obs = pd.read_csv(TRAIN_DIR / "synop_obs.csv", dtype={"synop_wmo": str}, encoding="utf-8-sig")
    airports = load_airports()[["icao", "region", "lat", "lon"]]
    table = (feats[feats["run"].astype(str) == run]
             .merge(obs, on=["date", "icao"]).merge(airports, on="icao")
             .dropna(subset=["obs24_mm", "point_mm"]))
    # AWOS at the airport is the preferred truth; SYNOP within 15 km fills days and airports without AWOS
    awos = load_awos().rename("awos_mm").reset_index()
    table = table.merge(awos, on=["date", "icao"], how="left")
    has_awos = table["awos_mm"].notna()
    table = table.assign(obs24_mm=table["awos_mm"].where(has_awos, table["obs24_mm"]),
                         truth=np.where(has_awos, "awos", "synop"))
    table = table[has_awos | table["synop_is_near"].astype(bool)] if near_only else table
    table = table.dropna(subset=["obs24_mm"])
    doy = pd.to_datetime(table["date"]).dt.dayofyear
    regions = pd.get_dummies(table["region"], prefix="rg", dtype=float)
    table = pd.concat([table.assign(doy_sin=np.sin(2 * np.pi * doy / 365.25), doy_cos=np.cos(2 * np.pi * doy / 365.25)),
                       regions], axis=1)
    week = pd.to_datetime(table["date"]).dt.isocalendar().week.astype(int)
    return table.assign(week=week).reset_index(drop=True), list(regions.columns)


def fit_bias(train):
    by_region = train.groupby("region").apply(lambda g: g["obs24_mm"].sum() / max(g["point_mm"].sum(), 1e-6),
                                              include_groups=False)
    overall = train["obs24_mm"].sum() / max(train["point_mm"].sum(), 1e-6)
    return {"overall": float(overall), **{k: float(v) for k, v in by_region.items()}}


def apply_bias(params, frame):
    factor = frame["region"].map(params).fillna(params["overall"])
    return (frame["point_mm"] * factor).clip(lower=0)


def fit_qm(train):
    return {"fc": np.quantile(train["point_mm"], QM_QUANTILES).tolist(),
            "obs": np.quantile(train["obs24_mm"], QM_QUANTILES).tolist()}


def apply_qm(params, frame):
    fc, obs = np.array(params["fc"]), np.array(params["obs"])
    # flat stretches of the forecast CDF (many zeros) map to the mean of the matching obs quantiles
    unique_fc, inverse = np.unique(fc, return_inverse=True)
    unique_obs = np.bincount(inverse, weights=obs) / np.bincount(inverse)
    return pd.Series(np.interp(frame["point_mm"], unique_fc, unique_obs), index=frame.index).clip(lower=0)


def features(frame, regions):
    return frame[NUMERIC + regions].astype(float)


def fit_rf(train, regions):
    model = RandomForestRegressor(n_estimators=400, min_samples_leaf=5, max_features=0.5, random_state=0, n_jobs=-1)
    return model.fit(features(train, regions), np.log1p(train["obs24_mm"]))


def fit_xgb(train, regions):
    model = XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8,
                         min_child_weight=5, reg_lambda=1.0, random_state=0)
    return model.fit(features(train, regions), np.log1p(train["obs24_mm"]))


def predict_ml(model, frame, regions):
    return pd.Series(np.expm1(model.predict(features(frame, regions))), index=frame.index).clip(lower=0)


METHODS = {
    "raw": (lambda train, regions: None, lambda m, frame, regions: frame["point_mm"]),
    "bias_region": (lambda train, regions: fit_bias(train), lambda m, frame, regions: apply_bias(m, frame)),
    "quantile_map": (lambda train, regions: fit_qm(train), lambda m, frame, regions: apply_qm(m, frame)),
    "random_forest": (fit_rf, predict_ml),
    "xgboost": (fit_xgb, predict_ml),
}


def cross_validate(table, regions):
    folds = GroupKFold(n_splits=min(FOLDS, table["week"].nunique())).split(table, groups=table["week"])
    preds = pd.DataFrame(index=table.index, columns=list(METHODS), dtype=float)
    for train_idx, test_idx in folds:
        train, test = table.loc[train_idx], table.loc[test_idx]
        for name, (fit, predict) in METHODS.items():
            preds.loc[test_idx, name] = predict(fit(train, regions), test, regions).values
    return preds


def category(values):
    return np.searchsorted(CAT_BOUNDS, values, side="right")


def score(f, o):
    hit = lambda t: int(((f >= t) & (o >= t)).sum())
    miss = lambda t: int(((f < t) & (o >= t)).sum())
    fa = lambda t: int(((f >= t) & (o < t)).sum())
    csi = lambda t: hit(t) / max(hit(t) + miss(t) + fa(t), 1)
    return {"MAE": float((f - o).abs().mean()), "RMSE": float(np.sqrt(((f - o) ** 2).mean())),
            "bias": float((f - o).mean()), "cat_match": float((category(f) == category(o)).mean()),
            "CSI≥0.1": csi(0.1), "CSI≥10": csi(10.0), "hit/miss/fa≥10": f"{hit(10.0)}/{miss(10.0)}/{fa(10.0)}"}


def markdown_table(frame):
    cells = [[str(c) for c in frame.columns]] + [[f"{v:.2f}" if isinstance(v, float) else str(v) for v in row]
                                                  for row in frame.itertuples(index=False)]
    lines = ["| " + " | ".join(r) + " |" for r in cells]
    return "\n".join([lines[0], "|" + "---|" * len(frame.columns), *lines[1:]])


def save_final_models(table, regions):
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    (MODEL_DIR / "bias_region.json").write_text(json.dumps(fit_bias(table), indent=2), encoding="utf-8")
    (MODEL_DIR / "quantile_map.json").write_text(json.dumps(fit_qm(table)), encoding="utf-8")
    joblib.dump({"model": fit_rf(table, regions), "features": NUMERIC + regions}, MODEL_DIR / "random_forest.joblib")
    joblib.dump({"model": fit_xgb(table, regions), "features": NUMERIC + regions}, MODEL_DIR / "xgboost.joblib")


def main():
    parser = argparse.ArgumentParser(description="Cross-validate simple and ML corrections of WRFDA 24 h rain against SYNOP")
    parser.add_argument("--run", default="12", choices=["12", "18"])
    parser.add_argument("--all-stations", action="store_true", help="include SYNOP stations farther than 15 km")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    table, regions = load_table(args.run, not args.all_stations)
    preds = cross_validate(table, regions)
    pd.concat([table[["date", "icao", "region", "obs24_mm"]], preds.round(2)], axis=1).to_csv(
        PREDICTIONS, index=False, encoding="utf-8-sig")
    results = pd.DataFrame([{"method": name, **score(preds[name], table["obs24_mm"])} for name in METHODS])
    save_final_models(table, regions)
    lines = [
        f"# WRFDA {args.run} UTC correction — cross-validated against SYNOP",
        "",
        f"{len(table)} airport-days, {table['date'].nunique()} days ({table['date'].min()} to {table['date'].max()}), "
        f"{table['icao'].nunique()} airports{'' if args.all_stations else ' with SYNOP within 15 km'}; "
        f"rain ≥10 mm observed {int((table['obs24_mm'] >= 10).sum())} times. "
        f"{FOLDS}-fold CV grouped by ISO week (test weeks never seen in training). "
        f"Updated {datetime.now(BANGKOK):%Y-%m-%d %H:%M} ICT.",
        "",
        markdown_table(results),
        "",
        "raw = nearest grid point; bias_region = per-region multiplicative factor; quantile_map = empirical CDF mapping; "
        "random_forest / xgboost = predict log(1+obs) from point and neighbourhood (9/21/45 km) features, region, location, season.",
        "",
        "Small sample: treat differences of a few hundredths as noise. Re-run as more days accumulate.",
    ]
    RESULTS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
