import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import numpy as np
import pandas as pd
import requests

from common import HERE, date_range, load_airports, period_start_utc
from fetch_synop_24h import process_date as fetch_synop
from fetch_wrfda_24h import accumulate_24h, download, run_tag

log = logging.getLogger("training")

TRAIN_DIR = HERE / "training"
WRFDA_FEATURES = TRAIN_DIR / "wrfda_features.csv"
SYNOP_OBS = TRAIN_DIR / "synop_obs.csv"
RUN_OFFSETS_H = {"00": 24, "06": 18, "12": 12, "18": 6}
# half-widths in grid cells (~3 km): 3x3 ~9 km, 7x7 ~21 km, 15x15 ~45 km
RADII = (1, 3, 7)
WET_MM = (1.0, 10.0)
WORKERS = 4


def grid_index(total, airports):
    lons, lats = total["x"].values, total["y"].values
    ix = np.array([int(np.abs(lons - lon).argmin()) for lon in airports["lon"]])
    iy = np.array([int(np.abs(lats - lat).argmin()) for lat in airports["lat"]])
    return ix, iy


def window(values, y, x, r):
    return values[max(y - r, 0): y + r + 1, max(x - r, 0): x + r + 1]


def airport_features(values, y, x):
    feats = {"point_mm": float(values[y, x])}
    for r in RADII:
        win = window(values, y, x, r)
        feats[f"mean_r{r}"] = float(win.mean())
        feats[f"max_r{r}"] = float(win.max())
    wide = window(values, y, x, RADII[-1])
    feats.update({f"wetfrac{t:g}_r{RADII[-1]}": float((wide >= t).mean()) for t in WET_MM})
    return feats


def run_features(local_date, run_label, airports):
    start = period_start_utc(local_date)
    run = start - timedelta(hours=RUN_OFFSETS_H[run_label])
    try:
        nc = download(run)
    except (requests.HTTPError, ValueError) as err:
        log.warning("%s %sZ not usable (%s)", local_date, run_label, err)
        return pd.DataFrame()
    total = accumulate_24h(nc, start)
    nc.unlink()
    values = total.values
    ix, iy = grid_index(total, airports)
    rows = [{"date": local_date, "run": run_label, "init": run_tag(run), "icao": icao,
             **{k: round(v, 3) for k, v in airport_features(values, y, x).items()}}
            for icao, y, x in zip(airports["icao"], iy, ix)]
    log.info("%s %sZ ok", local_date, run_label)
    return pd.DataFrame(rows)


def merge_into(path, new, key):
    old = pd.read_csv(path, dtype={"init": str, "run": str, "synop_wmo": str}, encoding="utf-8-sig") if path.exists() else new.iloc[0:0]
    # keys must share dtypes, otherwise rows never match and re-runs append duplicates
    new = new.astype({"run": str}) if "run" in new else new
    keep = old[~old.set_index(key).index.isin(new.set_index(key).index)] if len(new) else old
    merged = pd.concat([keep, new], ignore_index=True).drop_duplicates(key, keep="last").sort_values(key)
    merged.to_csv(path, index=False, encoding="utf-8-sig")
    return merged


def main():
    parser = argparse.ArgumentParser(description="Extract WRFDA 24 h features (12Z and 18Z) and SYNOP truth for model training")
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--skip-wrfda", action="store_true")
    parser.add_argument("--skip-synop", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    TRAIN_DIR.mkdir(parents=True, exist_ok=True)

    airports = load_airports()
    dates = date_range(args.start, args.end)
    jobs = [(d, r) for d in dates for r in RUN_OFFSETS_H]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        frames = [] if args.skip_wrfda else list(pool.map(lambda job: run_features(*job, airports), jobs))
    wrf = merge_into(WRFDA_FEATURES, pd.concat(frames, ignore_index=True), ["date", "run", "icao"]) if frames else None

    obs = [] if args.skip_synop else [fetch_synop(d, airports) for d in dates]
    syn = merge_into(SYNOP_OBS, pd.concat(obs, ignore_index=True)[
        ["date", "icao", "obs24_mm", "synop_wmo", "synop_dist_km", "synop_is_near", "decoded_from"]],
        ["date", "icao"]) if obs else None
    log.info("wrfda rows %s, synop rows %s", None if wrf is None else len(wrf), None if syn is None else len(syn))


if __name__ == "__main__":
    main()
