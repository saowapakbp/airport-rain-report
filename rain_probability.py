import logging

import joblib
import numpy as np
import pandas as pd

from build_training_set import airport_features, grid_index
from common import HERE
from train_probability import design

log = logging.getLogger("prob")

MODEL_PATH = HERE / "training" / "models" / "prob10.joblib"
# cross-validated reliability is good below ~50 % and overconfident above, so values are shown to the nearest 10 %
ROUND_TO = 10


def probability_percent(total, airports, local_date):
    bundle = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else {"deploy": False}
    if not bundle["deploy"]:
        log.info("probability model not deployed")
        return {}
    ix, iy = grid_index(total, airports)
    values = total.values
    rows = pd.DataFrame([airport_features(values, y, x) for y, x in zip(iy, ix)], index=airports.index)
    doy = pd.Timestamp(local_date).dayofyear
    frame = pd.concat([airports[["icao", "region", "lat", "lon"]], rows], axis=1).assign(
        doy_sin=np.sin(2 * np.pi * doy / 365.25), doy_cos=np.cos(2 * np.pi * doy / 365.25))
    frame = pd.concat([frame, pd.get_dummies(frame["region"], prefix="rg", dtype=float)], axis=1)
    p = bundle["model"].predict_proba(design(frame, bundle["regions"]))[:, 1]
    percent = (np.round(p * 100 / ROUND_TO) * ROUND_TO).astype(int)
    return dict(zip(frame["icao"], percent.tolist()))
