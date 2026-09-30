import argparse
import logging
import re
from datetime import timedelta

import pandas as pd
import requests

from common import DATA_DIR, categorize, date_range, load_airports, period_start_utc

log = logging.getLogger("synop")

GTS_URL = "http://203.155.200.113/php/AllData.php"
GTS_HOST = "gts.tmd.go.th"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
OUT_DIR = DATA_DIR / "synop_24h_airports"
TRACE_MM = 0.0
SECTION_END = {"222", "333", "444", "555"}


def fetch_bulletin(obs_time):
    params = {"alldate": f"/Synoptic/{obs_time:%d}-{MONTHS[obs_time.month - 1]}{obs_time:%y}.T{obs_time:%H}",
              "tyear": obs_time.year + 543}
    response = requests.get(GTS_URL, params=params, headers={"Host": GTS_HOST}, timeout=30)
    response.raise_for_status()
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", response.text).replace("&nbsp;", " "))


def split_reports(text):
    reports = {}
    for chunk in text.split("="):
        tokens = chunk.split()
        body = tokens[tokens.index("AAXX") + 2:] if "AAXX" in tokens else tokens
        # NIL placeholders are skipped; later delayed/corrected bulletins (RRx, CCx) overwrite earlier reports
        if len(body) > 1 and body[1] != "NIL" and re.fullmatch(r"48[3-5]\d\d", body[0]):
            reports[body[0]] = body
    return reports


def until_next_section(groups):
    stop = next((i for i, tok in enumerate(groups) if tok in SECTION_END), len(groups))
    return groups[:stop]


def section3(tokens):
    return until_next_section(tokens[tokens.index("333") + 1:]) if "333" in tokens else []


def rrr_to_mm(rrr):
    return TRACE_MM if rrr == 990 else (rrr - 990) / 10.0 if rrr > 990 else float(rrr)


def from_group7(section3):
    value = next((tok[1:] for tok in section3 if re.fullmatch(r"7\d{4}", tok)), None)
    return None if value is None else (TRACE_MM if value == "9999" else int(value) / 10.0)


def from_group6(section1):
    match = next((m for m in (re.fullmatch(r"6(\d{3})4", tok) for tok in section1) if m), None)
    return None if match is None else rrr_to_mm(int(match.group(1)))


def from_indicator(tokens):
    # iR = 3 means "no precipitation" so group 6 is intentionally omitted
    return 0.0 if len(tokens) > 1 and tokens[1][:1] == "3" else None


def decode_24h(tokens):
    candidates = [("333_7RRRR", from_group7(section3(tokens))),
                  ("6RRR4", from_group6(until_next_section(tokens[1:]))),
                  ("iR=3", from_indicator(tokens))]
    return next(((src, mm) for src, mm in candidates if mm is not None), (None, None))


def airport_rows(local_date, airports, reports):
    rows = []
    for a in airports.itertuples():
        tokens = reports.get(a.synop_wmo, [])
        source, mm = decode_24h(tokens) if tokens else (None, None)
        rows.append({"date": local_date, "icao": a.icao, "synop_wmo": a.synop_wmo, "synop_name": a.synop_name,
                     "synop_dist_km": a.synop_dist_km, "synop_is_near": a.synop_is_near,
                     "obs24_mm": mm, "category": categorize(mm), "decoded_from": source,
                     "report": " ".join(tokens)[:120]})
    return rows


def process_date(local_date, airports):
    obs_time = period_start_utc(local_date) + timedelta(days=1)
    reports = split_reports(fetch_bulletin(obs_time))
    frame = pd.DataFrame(airport_rows(local_date, airports, reports))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"synop_24h_airports_{local_date}.csv"
    frame.to_csv(out, index=False, encoding="utf-8-sig")
    log.info("%s: %d/%d airports decoded -> %s", local_date, frame["obs24_mm"].notna().sum(), len(frame), out.name)
    return frame


def main():
    parser = argparse.ArgumentParser(description="GTS SYNOP 24 h rainfall ending 07:00 local (00 UTC) at airports")
    parser.add_argument("--start", required=True, help="period start date YYYY-MM-DD (07:00 local)")
    parser.add_argument("--end", help="last period start date YYYY-MM-DD (default: --start)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    airports = load_airports()
    frames = [process_date(d, airports) for d in date_range(args.start, args.end)]
    summary = pd.concat(frames, ignore_index=True)
    print(summary[["date", "icao", "synop_wmo", "obs24_mm", "decoded_from"]].to_string(index=False))


if __name__ == "__main__":
    main()
