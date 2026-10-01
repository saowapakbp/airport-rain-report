import argparse
import logging
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import xarray as xr
from ecmwf.opendata import Client

from common import DATA_DIR, categorize, load_airports, period_start_utc
from fetch_wrfda_24h import POINT_DIR, process_date

log = logging.getLogger("ifs")

IFS_DIR = DATA_DIR / "ecmwf_ifs"
OUT_DIR = DATA_DIR / "compare"
M_TO_MM = 1000.0


def download_tp(run, steps):
    IFS_DIR.mkdir(parents=True, exist_ok=True)
    target = IFS_DIR / f"ifs_tp_{run:%Y%m%d%H}_{steps[0]}-{steps[1]}.grib2"
    if not target.exists():
        Client(source="ecmwf").retrieve(date=run.strftime("%Y%m%d"), time=run.hour, step=list(steps),
                                         type="fc", param="tp", target=str(target))
    return target


def ifs_24h(grib, steps):
    with xr.open_dataset(grib, engine="cfgrib", backend_kwargs={"indexpath": ""}) as ds:
        tp = ds["tp"].load()
    step_hours = (tp["step"].values / np.timedelta64(1, "h")).astype(int)
    first, last = (tp.isel(step=int(np.where(step_hours == h)[0][0])) for h in steps)
    return ((last - first) * M_TO_MM).clip(min=0)


def at_airports(field, airports):
    lons = field["longitude"].values
    lats = field["latitude"].values
    values = field.values
    ix = [int(np.abs(((lons - lon + 180) % 360) - 180).argmin()) for lon in airports["lon"]]
    iy = [int(np.abs(lats - lat).argmin()) for lat in airports["lat"]]
    return [round(float(values[y, x]), 1) for y, x in zip(iy, ix)]


def wrfda_points(local_date, run, airports):
    path = POINT_DIR / f"wrfda_d02_24h_airports_{local_date}_run{run:%Y%m%d%H}.csv"
    return pd.read_csv(path, encoding="utf-8-sig") if path.exists() else process_date(local_date, run.replace(tzinfo=timezone.utc), False, airports)


def main():
    parser = argparse.ArgumentParser(description="Compare ECMWF IFS (open data, 0.25 deg) with WRFDA d02 at airports")
    parser.add_argument("--date", required=True, help="forecast date YYYY-MM-DD (07:00 to 07:00 local)")
    parser.add_argument("--run", required=True, help="model init YYYYMMDDHH (UTC), 00 or 12")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    airports = load_airports()
    run = datetime.strptime(args.run, "%Y%m%d%H")
    start = period_start_utc(args.date).replace(tzinfo=None)
    lead = int((start - run) / timedelta(hours=1))
    steps = (lead, lead + 24)
    ifs = at_airports(ifs_24h(download_tp(run, steps), steps), airports)
    wrf = wrfda_points(args.date, run, airports).set_index("icao")["rain24_mm"]
    table = airports[["icao", "name_th", "region"]].assign(
        wrfda_mm=[float(wrf.get(i, np.nan)) for i in airports["icao"]],
        ifs_mm=ifs,
    ).assign(diff_mm=lambda d: (d["ifs_mm"] - d["wrfda_mm"]).round(1),
             wrfda_cat=lambda d: d["wrfda_mm"].map(categorize),
             ifs_cat=lambda d: d["ifs_mm"].map(categorize))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"wrfda_vs_ifs_{args.date}_run{args.run}.csv"
    table.to_csv(out, index=False, encoding="utf-8-sig")
    log.info("steps %s-%s h -> %s", *steps, out.name)
    print(table.drop(columns=["name_th"]).to_string(index=False))


if __name__ == "__main__":
    main()
