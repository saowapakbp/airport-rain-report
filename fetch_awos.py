import argparse
import logging
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests
import urllib3

from common import HERE, date_range

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = logging.getLogger("awos")

API = "https://aeromet2.tmd.go.th/api/daily-obs/rainfall-report"
AWOS_HISTORY = HERE / "verification" / "awos_history.csv"
BANGKOK = timezone(timedelta(hours=7))
# airport forecasters started entering AWOS rainfall on this date; earlier API values are not trusted
FIRST_ENTRY_DATE = "2026-09-28"
# late entries can arrive days afterwards, so recent days are re-fetched every run
REFRESH_DAYS = 7
TRACE_MM = 0.05
KEY = ["date", "icao"]


def fetch_day(local_date):
    response = requests.get(API, params={"date": local_date}, timeout=30, verify=False)
    body = response.json()
    if "error" in body:
        log.info("%s: %s", local_date, body["error"].get("code"))
        return pd.DataFrame()
    rows = [{"date": local_date, "icao": s["icao"], "status": s["status"], "band": s.get("band"),
             "awos_mm": TRACE_MM if s["status"] == "trace" else s.get("rainMm"), "label": s.get("label"),
             "issued_at": body.get("issuedAt")} for s in body["stations"]]
    return pd.DataFrame(rows)


def merge_history(new):
    old = pd.read_csv(AWOS_HISTORY, encoding="utf-8-sig") if AWOS_HISTORY.exists() else new.iloc[0:0]
    merged = pd.concat([old, new], ignore_index=True).drop_duplicates(KEY, keep="last").sort_values(KEY)
    AWOS_HISTORY.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(AWOS_HISTORY, index=False, encoding="utf-8-sig")
    return merged


def load_awos():
    # numeric AWOS rain per (date, icao); missing/fault rows are NaN
    if not AWOS_HISTORY.exists():
        return pd.Series(dtype=float, name="awos_mm")
    awos = pd.read_csv(AWOS_HISTORY, encoding="utf-8-sig")
    return pd.to_numeric(awos.set_index(KEY)["awos_mm"], errors="coerce")


def main():
    yesterday = (datetime.now(BANGKOK) - timedelta(days=1)).strftime("%Y-%m-%d")
    default_start = max(FIRST_ENTRY_DATE, (datetime.now(BANGKOK) - timedelta(days=REFRESH_DAYS)).strftime("%Y-%m-%d"))
    parser = argparse.ArgumentParser(description="Fetch AWOS 24 h rainfall (07:00-07:00 ICT) from the aeromet2 public API")
    parser.add_argument("--start", default=default_start)
    parser.add_argument("--end", default=yesterday)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    frames = [fetch_day(d) for d in date_range(max(args.start, FIRST_ENTRY_DATE), args.end)]
    new = pd.concat(frames, ignore_index=True) if any(len(f) for f in frames) else pd.DataFrame()
    history = merge_history(new) if len(new) else None
    log.info("fetched %d rows, history %s rows", len(new), None if history is None else len(history))


if __name__ == "__main__":
    main()
