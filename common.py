from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
AIRPORTS_CSV = HERE / "airports.csv"

# Upper bounds (exclusive) of the TMD 24 h rainfall categories, in mm
CATEGORIES = [
    ("none", 0.1),
    ("light", 10.05),
    ("mod", 35.05),
    ("heavy", 90.05),
    ("extreme", float("inf")),
]
NEAR_STATION_KM = 15.0


def load_airports():
    airports = pd.read_csv(AIRPORTS_CSV, dtype={"synop_wmo": str}, encoding="utf-8-sig")
    return airports.assign(synop_is_near=airports["synop_dist_km"] <= NEAR_STATION_KM)


def categorize(mm):
    return None if pd.isna(mm) else next(key for key, upper in CATEGORIES if mm < upper)


def period_start_utc(local_date):
    # 07:00 local (UTC+7) equals 00 UTC of the same calendar date
    return datetime.strptime(local_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def date_range(start, end):
    first = datetime.strptime(start, "%Y-%m-%d")
    days = (datetime.strptime(end or start, "%Y-%m-%d") - first).days
    return [(first + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days + 1)]
