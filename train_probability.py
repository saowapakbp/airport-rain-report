import argparse
import logging
from datetime import datetime, timedelta, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from common import HERE
from train_correction import FOLDS, load_table, markdown_table

log = logging.getLogger("prob")

TRAIN_DIR = HERE / "training"
MODEL_PATH = TRAIN_DIR / "models" / "prob10.joblib"
RESULTS = TRAIN_DIR / "results_prob10.md"
BANGKOK = timezone(timedelta(hours=7))
THRESHOLD_MM = 10.0
MM_FEATURES = ["point_mm", "mean_r1", "max_r1", "mean_r3", "max_r3", "mean_r7", "max_r7"]
OTHER_FEATURES = ["wetfrac1_r7", "wetfrac10_r7", "lat", "lon", "doy_sin", "doy_cos"]
RELIABILITY_BINS = np.array([0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0001])
# deploy only if cross-validated Brier skill vs climatology is at least this
MIN_BSS = 0.05


def design(frame, regions):
    logs = np.log1p(frame[MM_FEATURES].clip(lower=0)).add_prefix("log_")
    return pd.concat([logs, frame[OTHER_FEATURES], frame.reindex(columns=regions, fill_value=0.0)], axis=1).astype(float)


MODELS = {
    "logistic": lambda: make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=2000)),
    "random_forest": lambda: RandomForestClassifier(n_estimators=400, min_samples_leaf=10, max_features=0.5,
                                                    random_state=0, n_jobs=-1),
    "xgboost": lambda: XGBClassifier(n_estimators=250, max_depth=3, learning_rate=0.05, subsample=0.8,
                                     colsample_bytree=0.8, min_child_weight=10, random_state=0),
}
BASELINES = {
    "raw point ≥10 (0/1)": lambda f: (f["point_mm"] >= THRESHOLD_MM).astype(float),
    "neighbourhood fraction 45 km": lambda f: f["wetfrac10_r7"],
}


def cross_validate(table, regions):
    target = (table["obs24_mm"] >= THRESHOLD_MM).astype(int)
    folds = GroupKFold(n_splits=min(FOLDS, table["week"].nunique())).split(table, groups=table["week"])
    probs = pd.DataFrame(index=table.index, columns=[*MODELS, "climatology"], dtype=float)
    for train_idx, test_idx in folds:
        x_train, x_test = design(table.loc[train_idx], regions), design(table.loc[test_idx], regions)
        for name, make in MODELS.items():
            model = make().fit(x_train, target.loc[train_idx])
            probs.loc[test_idx, name] = model.predict_proba(x_test)[:, 1]
        probs.loc[test_idx, "climatology"] = target.loc[train_idx].mean()
    for name, rule in BASELINES.items():
        probs[name] = rule(table).values
    return probs, target


def score(p, y, clim_brier):
    brier = brier_score_loss(y, p)
    return {"Brier": brier, "BSS vs climatology": 1 - brier / clim_brier, "AUC": roc_auc_score(y, p),
            "mean prob": float(p.mean()), "observed rate": float(y.mean())}


def reliability(p, y):
    bins = pd.cut(p, RELIABILITY_BINS, right=False)
    table = pd.DataFrame({"p": p, "y": y, "bin": bins}).groupby("bin", observed=True).agg(
        forecasts=("p", "size"), mean_forecast=("p", "mean"), observed_freq=("y", "mean"))
    return table.reset_index().assign(bin=lambda t: t["bin"].astype(str))


def main():
    parser = argparse.ArgumentParser(description="Train and cross-validate P(24 h rain >= 10 mm) at airports")
    parser.add_argument("--run", default="12", choices=["12", "18"])
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    table, regions = load_table(args.run, True)
    probs, target = cross_validate(table, regions)
    clim_brier = brier_score_loss(target, probs["climatology"])
    scores = pd.DataFrame([{"method": name, **score(probs[name], target, clim_brier)} for name in probs.columns])
    best = scores[scores["method"].isin(list(MODELS))].sort_values("BSS vs climatology", ascending=False).iloc[0]
    deploy = bool(best["BSS vs climatology"] >= MIN_BSS)
    final = MODELS[best["method"]]().fit(design(table, regions), target)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": final, "method": best["method"], "regions": regions, "deploy": deploy,
                 "cv_bss": float(best["BSS vs climatology"]), "trained": f"{datetime.now(BANGKOK):%Y-%m-%d}",
                 "days": int(table["date"].nunique()), "run": args.run}, MODEL_PATH)
    lines = [
        f"# P(24 h rain ≥ {THRESHOLD_MM:g} mm) — WRFDA {args.run} UTC, cross-validated against AWOS (SYNOP where no AWOS)",
        "",
        f"{len(table)} airport-days, {table['date'].nunique()} days ({table['date'].min()} to {table['date'].max()}), "
        f"{int(target.sum())} events ({target.mean():.0%}). {FOLDS}-fold CV grouped by ISO week. "
        f"Updated {datetime.now(BANGKOK):%Y-%m-%d %H:%M} ICT.",
        "",
        markdown_table(scores),
        "",
        f"Best model: **{best['method']}** (BSS {best['BSS vs climatology']:.2f}). "
        f"Shown in the daily report: **{'yes' if deploy else 'no'}** (needs BSS ≥ {MIN_BSS}).",
        "",
        f"## Reliability of {best['method']} (cross-validated)",
        "",
        markdown_table(reliability(probs[best["method"]], target)),
        "",
        "BSS > 0 means better than always forecasting the historical event rate; AUC 0.5 = no skill, 1 = perfect ranking.",
    ]
    RESULTS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
