import argparse
import logging
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests

from common import CATEGORIES, HERE, categorize, load_airports, period_start_utc
from fetch_awos import load_awos
from compare_ecmwf_ifs import at_airports, download_tp, ifs_24h
from fetch_synop_24h import process_date as fetch_synop
from fetch_wrfda_24h import process_date as fetch_wrfda

log = logging.getLogger("verify")

VERIFY_DIR = HERE / "verification"
HISTORY = VERIFY_DIR / "verify_history.csv"
SUMMARY = VERIFY_DIR / "summary.md"
BANGKOK = timezone(timedelta(hours=7))
MODELS = {"wrfda12_mm": "WRFDA 12 UTC (19:00 ICT)", "wrfda18_mm": "WRFDA 18 UTC (01:00 ICT)",
          "ifs12_mm": "ECMWF IFS 12 UTC (0.25°)"}
TRUTHS = {"awos_mm": "AWOS (airport)", "obs24_mm": "SYNOP (nearest station)"}
THRESHOLDS_MM = (0.1, 10.0, 35.1)
KEY = ["date", "icao"]


def run_before(local_date, hours):
    return period_start_utc(local_date) - timedelta(hours=hours)


def wrfda_column(local_date, offset_h, airports):
    try:
        points = fetch_wrfda(local_date, run_before(local_date, offset_h), False, airports)
        return points.set_index("icao")["rain24_mm"]
    except (requests.HTTPError, ValueError) as err:
        log.warning("WRFDA run %s not usable (%s)", run_before(local_date, offset_h), err)
        return pd.Series(dtype=float)


def ifs_column(local_date, airports):
    run = run_before(local_date, 12).replace(tzinfo=None)
    steps = (12, 36)
    return pd.Series(at_airports(ifs_24h(download_tp(run, steps), steps), airports), index=airports["icao"])


AWOS = load_awos()


def awos_column(local_date):
    awos = AWOS
    return awos.xs(local_date, level="date") if local_date in awos.index.get_level_values("date") else pd.Series(dtype=float)


def verify_day(local_date, airports):
    obs = fetch_synop(local_date, airports).set_index("icao")
    frame = airports[["icao", "region"]].set_index("icao").assign(
        date=local_date,
        wrfda12_mm=wrfda_column(local_date, 12, airports),
        wrfda18_mm=wrfda_column(local_date, 6, airports),
        ifs12_mm=ifs_column(local_date, airports),
        obs24_mm=obs["obs24_mm"],
        awos_mm=awos_column(local_date),
        synop_wmo=obs["synop_wmo"],
        synop_dist_km=obs["synop_dist_km"],
        synop_is_near=obs["synop_is_near"],
    )
    return frame.reset_index()


def append_history(day):
    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    old = pd.read_csv(HISTORY, dtype={"synop_wmo": str}, encoding="utf-8-sig") if HISTORY.exists() else day.iloc[0:0]
    merged = pd.concat([old[~old.set_index(KEY).index.isin(day.set_index(KEY).index)], day], ignore_index=True)
    merged.sort_values(KEY).to_csv(HISTORY, index=False, encoding="utf-8-sig")
    return merged


def refresh_awos(history):
    days = [awos_column(d).rename("awos_mm").to_frame().assign(date=d).reset_index() for d in history["date"].unique()]
    awos = pd.concat(days, ignore_index=True) if days else pd.DataFrame(columns=["icao", "awos_mm", "date"])
    return history.drop(columns=["awos_mm"]).merge(awos, on=KEY, how="left")


def scores(f, o):
    err = f - o
    row = {"n": len(o), "bias": err.mean(), "MAE": err.abs().mean(), "RMSE": float(np.sqrt((err ** 2).mean())),
           "cat_match": float(np.mean([categorize(a) == categorize(b) for a, b in zip(f, o)]))}
    for t in THRESHOLDS_MM:
        hit, miss, fa = ((f >= t) & (o >= t)).sum(), ((f < t) & (o >= t)).sum(), ((f >= t) & (o < t)).sum()
        row[f"POD≥{t:g}"] = hit / max(hit + miss, 1)
        row[f"FAR≥{t:g}"] = fa / max(hit + fa, 1)
        row[f"CSI≥{t:g}"] = hit / max(hit + miss + fa, 1)
        row[f"obs≥{t:g}"] = int((o >= t).sum())
    return row


def score_table(history):
    rows = []
    for truth, truth_label in TRUTHS.items():
        for col, label in MODELS.items():
            pair = history.dropna(subset=[truth, col])
            rows.append({"truth": truth_label, "model": label, "days": pair["date"].nunique(),
                         **scores(pair[col], pair[truth])}) if len(pair) else None
    return pd.DataFrame(rows)


def markdown_table(frame):
    cells = [[str(c) for c in frame.columns]] + [[f"{v:.2f}" if isinstance(v, float) else str(v) for v in row]
                                                  for row in frame.itertuples(index=False)]
    lines = ["| " + " | ".join(r) + " |" for r in cells]
    return "\n".join([lines[0], "|" + "---|" * len(frame.columns), *lines[1:]])


def write_summary(history):
    table = score_table(history)
    by_region = history.groupby("region")[[*MODELS, *TRUTHS]].mean().round(1).reset_index()
    lines = [
        "# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP",
        "",
        f"24 h rainfall 07:00–07:00 ICT at {history['icao'].nunique()} airports · {history['date'].nunique()} days "
        f"({history['date'].min()} to {history['date'].max()}) · updated {datetime.now(BANGKOK):%Y-%m-%d %H:%M} ICT",
        "",
        "Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); "
        "SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).",
        "",
        "## Scores",
        "",
        markdown_table(table) if len(table) else "No pairs yet.",
        "",
        "## Mean 24 h rain by region (mm)",
        "",
        markdown_table(by_region),
        "",
        f"Categories: {', '.join(f'{k} < {v:g}' for k, v in CATEGORIES[:-1])} mm. "
        "A few days of scores are noise; read them after a month or more.",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    yesterday = (datetime.now(BANGKOK) - timedelta(days=1)).strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description="Append a day of WRFDA 12/18 UTC and IFS vs AWOS/SYNOP and refresh the summary")
    parser.add_argument("--date", default=yesterday, help="period start date YYYY-MM-DD (default: yesterday, ICT)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    history = refresh_awos(append_history(verify_day(args.date, load_airports())))
    history.sort_values(KEY).to_csv(HISTORY, index=False, encoding="utf-8-sig")
    write_summary(history)
    log.info("%s done, history %d rows", args.date, len(history))
    print(history[history["date"] == args.date][["icao", *MODELS, *TRUTHS]].to_string(index=False))


if __name__ == "__main__":
    main()
