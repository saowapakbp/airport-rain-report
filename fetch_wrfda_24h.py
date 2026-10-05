import argparse
import logging
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests
import urllib3
import xarray as xr

from common import DATA_DIR, categorize, date_range, load_airports, period_start_utc

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = logging.getLogger("wrfda")

BASE_URL = "https://hpc.tmd.go.th/static/netcdf"
RAW_DIR = DATA_DIR / "wrfda_raw"
GRID_DIR = DATA_DIR / "wrfda_24h_grid"
POINT_DIR = DATA_DIR / "wrfda_24h_airports"
MIN_NC_BYTES = 1_000_000
# 12 UTC run of the previous day (19:00 ICT) is published about 03:30 ICT; 00 UTC is the fallback
RUN_OFFSETS_H = (12, 24)
NEIGHBOR_CELLS = 3


def run_tag(run):
    return run.strftime("%Y%m%d%H")


def download(run):
    tag = run_tag(run)
    out = RAW_DIR / f"{tag}.prec1hr.d02.nc"
    if out.exists() and out.stat().st_size > MIN_NC_BYTES:
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(f"{BASE_URL}/{tag}/{tag}.prec1hr.d02.nc", stream=True, verify=False, timeout=120)
    response.raise_for_status()
    part = out.with_suffix(".part")
    with open(part, "wb") as f:
        for chunk in response.iter_content(1 << 20):
            f.write(chunk)
    size = part.stat().st_size
    if size <= MIN_NC_BYTES:
        part.unlink()
        # TMD sometimes publishes a 0-byte file when a run fails; treat it like a missing run
        raise ValueError(f"{tag} is incomplete on the server ({size} bytes)")
    part.replace(out)
    log.info("downloaded %s (%.1f MB)", out.name, size / 1e6)
    return out


def download_first_available(start):
    for offset in RUN_OFFSETS_H:
        run = start - timedelta(hours=offset)
        try:
            return run, download(run)
        except (requests.HTTPError, ValueError) as err:
            log.warning("run %s not usable (%s)", run_tag(run), err)
    raise RuntimeError(f"no WRFDA run available for period starting {start:%Y-%m-%d %H} UTC")


def accumulate_24h(nc_path, start):
    t0 = np.datetime64(start.replace(tzinfo=None), "ns")
    with xr.open_dataset(nc_path, engine="scipy") as ds:
        window = ds["Total_precipitation"].sel(time=slice(t0 + np.timedelta64(1, "h"), t0 + np.timedelta64(24, "h")))
        hours = window.sizes["time"]
        if hours != 24:
            raise ValueError(f"{nc_path.name}: expected 24 hourly steps after {t0}, found {hours}")
        return window.sum("time").clip(min=0).load()


def save_grid(total, local_date, run):
    GRID_DIR.mkdir(parents=True, exist_ok=True)
    out = GRID_DIR / f"wrfda_d02_24h_{local_date}_run{run_tag(run)}.nc"
    total.rename("rain24_mm").assign_attrs(
        units="mm", period="07:00 local to 07:00 local next day", source="TMD WRFDA 3 km d02", run=run_tag(run)
    ).to_netcdf(out, engine="scipy")
    return out


def neighborhood_max(values, iy, ix):
    return float(values[max(iy - NEIGHBOR_CELLS, 0): iy + NEIGHBOR_CELLS + 1,
                        max(ix - NEIGHBOR_CELLS, 0): ix + NEIGHBOR_CELLS + 1].max())


def extract_airports(total, airports):
    lons, lats, values = total["x"].values, total["y"].values, total.values
    ix = [int(np.abs(lons - lon).argmin()) for lon in airports["lon"]]
    iy = [int(np.abs(lats - lat).argmin()) for lat in airports["lat"]]
    point = [round(float(values[y, x]), 1) for y, x in zip(iy, ix)]
    return airports[["icao", "name_th", "region", "lat", "lon"]].assign(
        grid_lat=[round(float(lats[y]), 4) for y in iy],
        grid_lon=[round(float(lons[x]), 4) for x in ix],
        rain24_mm=point,
        rain24_nbr_max_mm=[round(neighborhood_max(values, y, x), 1) for y, x in zip(iy, ix)],
        category=[categorize(v) for v in point],
    )


def process_date(local_date, run_override, keep_raw, airports):
    start = period_start_utc(local_date)
    run, nc_path = (run_override, download(run_override)) if run_override else download_first_available(start)
    total = accumulate_24h(nc_path, start)
    grid_out = save_grid(total, local_date, run)
    points = extract_airports(total, airports).assign(date=local_date, run=run_tag(run),
                                                      lead_start_h=int((start - run).total_seconds() // 3600) + 1)
    POINT_DIR.mkdir(parents=True, exist_ok=True)
    point_out = POINT_DIR / f"wrfda_d02_24h_airports_{local_date}_run{run_tag(run)}.csv"
    points.to_csv(point_out, index=False, encoding="utf-8-sig")
    if not keep_raw:
        nc_path.unlink()
    log.info("%s run %s -> %s, %s", local_date, run_tag(run), grid_out.name, point_out.name)
    return points


def main():
    parser = argparse.ArgumentParser(description="TMD WRFDA d02 24 h rainfall (07:00-07:00 local) at airports")
    parser.add_argument("--start", required=True, help="forecast date YYYY-MM-DD (period starts 07:00 local)")
    parser.add_argument("--end", help="last forecast date YYYY-MM-DD (default: --start)")
    parser.add_argument("--run", help="force model run YYYYMMDDHH (UTC); default previous day 12 UTC, then 00 UTC")
    parser.add_argument("--keep-raw", action="store_true", help="keep the 58 MB hourly NetCDF")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    airports = load_airports()
    run = datetime.strptime(args.run, "%Y%m%d%H").replace(tzinfo=timezone.utc) if args.run else None
    frames = [process_date(d, run, args.keep_raw, airports) for d in date_range(args.start, args.end)]
    summary = pd.concat(frames, ignore_index=True)
    print(summary[["date", "icao", "rain24_mm", "rain24_nbr_max_mm", "category"]].to_string(index=False))


if __name__ == "__main__":
    main()
