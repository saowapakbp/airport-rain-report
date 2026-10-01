import argparse
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from common import CATEGORIES, HERE, categorize, load_airports, period_start_utc
from compare_ecmwf_ifs import at_airports, download_tp, ifs_24h
from fetch_synop_24h import process_date as fetch_synop
from fetch_wrfda_24h import process_date as fetch_wrfda

log = logging.getLogger("verify")

VERIFY_DIR = HERE / "verification"
HISTORY = VERIFY_DIR / "verify_history.csv"
SUMMARY = VERIFY_DIR / "summary.md"
BANGKOK = timezone(timedelta(hours=7))
MODELS = {"wrfda_mm": "WRFDA d02 (3 km)", "ifs_mm": "ECMWF IFS (0.25°)"}
THRESHOLDS_MM = (0.1, 10.0, 35.1)
KEY = ["date", "icao"]


def verify_day(local_date, airports):
    wrf = fetch_wrfda(local_date, None, False, airports)
    run_tag = wrf["run"].iloc[0]
    run = datetime.strptime(run_tag, "%Y%m%d%H")
    lead = int((period_start_utc(local_date).replace(tzinfo=None) - run) / timedelta(hours=1))
    steps = (lead, lead + 24)
    ifs = at_airports(ifs_24h(download_tp(run, steps), steps), airports)
    obs = fetch_synop(local_date, airports)
    return (airports[["icao", "region"]]
            .assign(date=local_date, run=run_tag, ifs_mm=ifs)
            .merge(wrf[["icao", "rain24_mm"]].rename(columns={"rain24_mm": "wrfda_mm"}), on="icao")
            .merge(obs[["icao", "obs24_mm", "synop_wmo", "synop_dist_km", "synop_is_near", "decoded_from"]], on="icao"))


def append_history(day):
    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    old = pd.read_csv(HISTORY, dtype={"synop_wmo": str}, encoding="utf-8-sig") if HISTORY.exists() else day.iloc[0:0]
    merged = pd.concat([old[~old.set_index(KEY).index.isin(day.set_index(KEY).index)], day], ignore_index=True)
    merged.sort_values(KEY).to_csv(HISTORY, index=False, encoding="utf-8-sig")
    return merged


def scores(f, o):
    err = f - o
    row = {"n": len(o), "bias": err.mean(), "MAE": err.abs().mean(), "RMSE": float(np.sqrt((err ** 2).mean())),
           "r": f.corr(o), "cat_match": float(np.mean([categorize(a) == categorize(b) for a, b in zip(f, o)]))}
    for t in THRESHOLDS_MM:
        hit, miss, fa = ((f >= t) & (o >= t)).sum(), ((f < t) & (o >= t)).sum(), ((f >= t) & (o < t)).sum()
        row[f"POD≥{t:g}"] = hit / max(hit + miss, 1)
        row[f"FAR≥{t:g}"] = fa / max(hit + fa, 1)
        row[f"CSI≥{t:g}"] = hit / max(hit + miss + fa, 1)
        row[f"obs≥{t:g}"] = int((o >= t).sum())
    return row


def score_table(history):
    valid = history.dropna(subset=["obs24_mm", *MODELS])
    subsets = {"ทุกสนามบิน": valid, "สถานีห่าง ≤ 15 กม.": valid[valid["synop_is_near"].astype(bool)]}
    rows = [{"ชุดข้อมูล": name, "แบบจำลอง": label, **scores(sub[col], sub["obs24_mm"])}
            for name, sub in subsets.items() for col, label in MODELS.items()]
    return pd.DataFrame(rows), valid["date"].nunique()


def markdown_table(frame):
    cells = [[str(c) for c in frame.columns]] + [[f"{v:.2f}" if isinstance(v, float) else str(v) for v in row]
                                                  for row in frame.itertuples(index=False)]
    lines = ["| " + " | ".join(r) + " |" for r in cells]
    return "\n".join([lines[0], "|" + "---|" * len(frame.columns), *lines[1:]])


def write_summary(history):
    table, days = score_table(history)
    by_region = (history.dropna(subset=["obs24_mm", *MODELS])
                 .groupby("region")[["wrfda_mm", "ifs_mm", "obs24_mm"]].mean().round(1))
    lines = [
        "# Verification: WRFDA vs ECMWF IFS vs SYNOP",
        "",
        f"24 h rainfall 07:00–07:00 local at {history['icao'].nunique()} airports · {days} days "
        f"({history['date'].min()} to {history['date'].max()}) · updated {datetime.now(BANGKOK):%Y-%m-%d %H:%M} ICT",
        "",
        "Truth: GTS SYNOP 24 h rain at 00 UTC (group 333 7RRRR). Both models use the run the daily report used "
        "(12 UTC previous day, 00 UTC fallback), nearest grid point. ECMWF open data (CC BY 4.0).",
        "",
        "## Scores",
        "",
        markdown_table(table),
        "",
        "## Mean 24 h rain by region (mm)",
        "",
        markdown_table(by_region.reset_index()),
        "",
        f"Categories: {', '.join(f'{k} < {v:g}' for k, v in CATEGORIES[:-1])} mm. One day of scores is noise; read them after a month or more.",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    yesterday = (datetime.now(BANGKOK) - timedelta(days=1)).strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description="Append yesterday's WRFDA/IFS vs SYNOP comparison and refresh the summary")
    parser.add_argument("--date", default=yesterday, help="period start date YYYY-MM-DD (default: yesterday, ICT)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    day = verify_day(args.date, load_airports())
    history = append_history(day)
    write_summary(history)
    log.info("%s: %d rows, history %d rows -> %s", args.date, len(day), len(history), Path(SUMMARY).name)
    print(day[["icao", "wrfda_mm", "ifs_mm", "obs24_mm"]].to_string(index=False))


if __name__ == "__main__":
    main()
