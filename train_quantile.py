import argparse
import logging
from datetime import datetime, timedelta, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import GroupKFold

from common import CATEGORIES, HERE, load_airports
from train_correction import markdown_table

log = logging.getLogger("quantile")

TRAIN_DIR = HERE / "training"
MODEL_PATH = TRAIN_DIR / "models" / "quantile.joblib"
RESULTS = TRAIN_DIR / "results_quantile.md"
PREDICTIONS = TRAIN_DIR / "cv_quantile.csv"
BANGKOK = timezone(timedelta(hours=7))
FOLDS = 5
QUANTILES = (0.1, 0.5, 0.9)
HEAVY_MM = 10.0
BIG_MM = 35.0
CAT_BOUNDS = [upper for _, upper in CATEGORIES[:-1]]
RUN_FEATURES = ["point_mm", "mean_r1", "max_r1", "mean_r3", "max_r3", "mean_r7", "max_r7", "wetfrac1_r7", "wetfrac10_r7"]
MM_FEATURES = ["point_mm", "mean_r1", "max_r1", "mean_r3", "max_r3", "mean_r7", "max_r7"]
DRY_MM = 0.1


def load_ensemble_table(runs=("12", "18")):
    feats = pd.read_csv(TRAIN_DIR / "wrfda_features.csv", dtype={"init": str, "run": str}, encoding="utf-8-sig")
    obs = pd.read_csv(TRAIN_DIR / "synop_obs.csv", dtype={"synop_wmo": str}, encoding="utf-8-sig")
    by_run = {r: feats[feats["run"] == r].set_index(["date", "icao"])[RUN_FEATURES].add_suffix(f"_{r}z") for r in runs}
    main = runs[-1]
    wide = by_run[main]
    # older runs are missing on a few days; fall back to the main run so the row is still usable
    for r in runs[:-1]:
        wide = wide.join(by_run[r], how="left")
        for col in RUN_FEATURES:
            wide[f"{col}_{r}z"] = wide[f"{col}_{r}z"].fillna(wide[f"{col}_{main}z"])
    for col in MM_FEATURES:
        members = wide[[f"{col}_{r}z" for r in runs]]
        wide[f"{col}_ensmean"] = members.mean(axis=1)
        wide[f"{col}_spread"] = members.max(axis=1) - members.min(axis=1)
    table = (wide.reset_index().merge(obs, on=["date", "icao"])
             .merge(load_airports()[["icao", "region", "lat", "lon"]], on="icao")
             .dropna(subset=["obs24_mm"]))
    table = table[table["synop_is_near"].astype(bool)]
    doy = pd.to_datetime(table["date"]).dt.dayofyear
    table = table.assign(doy_sin=np.sin(2 * np.pi * doy / 365.25), doy_cos=np.cos(2 * np.pi * doy / 365.25),
                         week=pd.to_datetime(table["date"]).dt.isocalendar().week.astype(int))
    regions = pd.get_dummies(table["region"], prefix="rg", dtype=float)
    return pd.concat([table, regions], axis=1).reset_index(drop=True), list(regions.columns)


def feature_columns(table, regions):
    model_cols = [c for c in table.columns if c.endswith(("_12z", "_18z", "_ensmean", "_spread"))]
    return model_cols + ["lat", "lon", "doy_sin", "doy_cos"] + regions


def design(frame, cols):
    out = frame.reindex(columns=cols, fill_value=0.0).astype(float).copy()
    mm = [c for c in cols if c.split("_")[0] in {"point", "mean", "max"} or c.startswith(("mean_", "max_"))]
    out[mm] = np.log1p(out[mm].clip(lower=0))
    return out


def fit_models(train, cols):
    x = design(train, cols)
    y = np.log1p(train["obs24_mm"])
    quantiles = {q: HistGradientBoostingRegressor(loss="quantile", quantile=q, max_iter=300, learning_rate=0.05,
                                                  max_leaf_nodes=15, min_samples_leaf=20, random_state=0).fit(x, y)
                 for q in QUANTILES}
    prob = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=20,
                                          random_state=0).fit(x, train["obs24_mm"] >= HEAVY_MM)
    return {"quantiles": quantiles, "prob": prob, "cols": cols}


def predict(bundle, frame):
    x = design(frame, bundle["cols"])
    q = np.sort(np.column_stack([np.expm1(bundle["quantiles"][k].predict(x)) for k in QUANTILES]).clip(min=0), axis=1)
    out = pd.DataFrame(q, columns=[f"q{int(k * 100)}" for k in QUANTILES], index=frame.index)
    return out.assign(prob10=bundle["prob"].predict_proba(x)[:, 1])


def baselines(table):
    point = table["point_mm_12z"]
    hybrid = table["mean_r7_12z"].where(point >= DRY_MM, point)
    ens = table["mean_r7_ensmean"].where(table["point_mm_ensmean"] >= DRY_MM, table["point_mm_ensmean"])
    return {"raw point 12Z": point, "report now (12Z area mean)": hybrid, "ensemble area mean": ens}


def amount_scores(f, o):
    hit = lambda t: int(((f >= t) & (o >= t)).sum())
    miss = lambda t: int(((f < t) & (o >= t)).sum())
    fa = lambda t: int(((f >= t) & (o < t)).sum())
    return {"MAE": float((f - o).abs().mean()), "bias": float((f - o).mean()),
            "cat_match": float((np.searchsorted(CAT_BOUNDS, f, side="right") == np.searchsorted(CAT_BOUNDS, o, side="right")).mean()),
            "CSI≥0.1": hit(0.1) / max(hit(0.1) + miss(0.1) + fa(0.1), 1),
            "CSI≥10": hit(HEAVY_MM) / max(hit(HEAVY_MM) + miss(HEAVY_MM) + fa(HEAVY_MM), 1),
            "≥10 hit/miss/fa": f"{hit(HEAVY_MM)}/{miss(HEAVY_MM)}/{fa(HEAVY_MM)}",
            "fc≥35 & obs<10": int(((f >= BIG_MM) & (o < HEAVY_MM)).sum())}


def pinball(q_pred, o, q):
    diff = o - q_pred
    return float(np.mean(np.maximum(q * diff, (q - 1) * diff)))


def cross_validate(table, cols):
    folds = GroupKFold(n_splits=min(FOLDS, table["week"].nunique())).split(table, groups=table["week"])
    parts = [predict(fit_models(table.iloc[tr], cols), table.iloc[te]) for tr, te in folds]
    return pd.concat(parts).sort_index()


def write_results(table, preds, old_prob):
    o = table["obs24_mm"]
    amount_rows = [{"method": k, **amount_scores(v, o)} for k, v in baselines(table).items()]
    amount_rows += [{"method": f"quantile model q{int(q * 100)}", **amount_scores(preds[f"q{int(q * 100)}"], o)} for q in QUANTILES]
    y = (o >= HEAVY_MM).astype(int)
    clim = brier_score_loss(y, np.full(len(y), y.mean()))
    prob_rows = [{"method": name, "Brier": brier_score_loss(y, p), "BSS": 1 - brier_score_loss(y, p) / clim,
                  "AUC": roc_auc_score(y, p)} for name, p in [("current logistic (12Z)", old_prob), ("new (12Z+18Z, GBM)", preds["prob10"])]]
    inside = ((o >= preds["q10"]) & (o <= preds["q90"])).mean()
    lines = [
        "# Stage 1 — distributional (quantile) correction of WRFDA 24 h rain, 12Z + 18Z",
        "",
        f"{len(table)} airport-days, {table['date'].nunique()} days ({table['date'].min()} to {table['date'].max()}), "
        f"SYNOP within 15 km; rain ≥10 mm observed {int(y.sum())} times. {FOLDS}-fold CV grouped by ISO week. "
        f"Updated {datetime.now(BANGKOK):%Y-%m-%d %H:%M} ICT.",
        "",
        "## Rain amount",
        "",
        markdown_table(pd.DataFrame(amount_rows)),
        "",
        f"Quantile loss (lower is better): q10 {pinball(preds['q10'], o, 0.1):.2f}, q50 {pinball(preds['q50'], o, 0.5):.2f}, "
        f"q90 {pinball(preds['q90'], o, 0.9):.2f}. Observed value inside the q10–q90 range: {inside:.0%} (ideal 80%).",
        "",
        "## P(rain ≥ 10 mm)",
        "",
        markdown_table(pd.DataFrame(prob_rows)),
    ]
    RESULTS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def old_probability(table):
    from train_probability import MODELS, design as old_design
    from train_correction import load_table
    old, regions = load_table("12", True)
    y = (old["obs24_mm"] >= HEAVY_MM).astype(int)
    probs = pd.Series(np.nan, index=old.index)
    for tr, te in GroupKFold(n_splits=min(FOLDS, old["week"].nunique())).split(old, groups=old["week"]):
        model = MODELS["logistic"]().fit(old_design(old.loc[tr], regions), y.loc[tr])
        probs.loc[te] = model.predict_proba(old_design(old.loc[te], regions))[:, 1]
    keyed = old.assign(p=probs).set_index(["date", "icao"])["p"]
    return table.set_index(["date", "icao"]).index.map(keyed).to_numpy(dtype=float)


def main():
    parser = argparse.ArgumentParser(description="Stage 1: quantile + probability model from a WRFDA run ensemble")
    parser.add_argument("--runs", default="00,06,12", help="comma-separated init hours, main run last (default: runs out before 07:00 ICT)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    table, regions = load_ensemble_table(tuple(args.runs.split(",")))
    cols = feature_columns(table, regions)
    preds = cross_validate(table, cols)
    pd.concat([table[["date", "icao", "region", "obs24_mm"]], preds.round(2)], axis=1).to_csv(PREDICTIONS, index=False, encoding="utf-8-sig")
    old_prob = old_probability(table)
    ok = ~np.isnan(old_prob)
    write_results(table[ok].reset_index(drop=True), preds[ok].reset_index(drop=True), old_prob[ok])
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({**fit_models(table, cols), "trained": f"{datetime.now(BANGKOK):%Y-%m-%d}", "deploy": False}, MODEL_PATH)


if __name__ == "__main__":
    main()
