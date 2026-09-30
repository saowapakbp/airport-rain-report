import argparse
import base64
import io
import json
import math
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import xarray as xr
from PIL import Image, ImageFilter

from common import HERE, load_airports
from fetch_wrfda_24h import GRID_DIR, process_date

log = logging.getLogger("report")

TEMPLATE = HERE / "report_template.html"
REPORT_DIR = HERE / "reports"
BANGKOK = timezone(timedelta(hours=7))
THAI_MONTHS = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
               "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
THAI_MONTHS_SHORT = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
                     "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
BUDDHIST_OFFSET = 543
VIEWPORT = (1560, 1000)
SCALE = 1.5
PREVIEW_WIDTH = 1040
# must match MAP in report_template.html
MAP_LON0, MAP_LAT1, MAP_K = 97.0, 20.7, 40.0
MAP_COS = math.cos(math.radians(13))
OVERLAY_UPSCALE = 3
LIGHT_ALPHA_MIN, LIGHT_ALPHA_MAX = 25, 150
EDGE_FADE_PX = 60
# (upper bound mm, RGBA) per rain class; values below 0.1 mm stay transparent
OVERLAY_COLORS = [
    (0.1, (0, 0, 0, 0)),
    (10.05, (79, 179, 238, 120)),
    (35.05, (26, 111, 207, 190)),
    (90.05, (242, 138, 26, 215)),
    (float("inf"), (217, 37, 59, 230)),
]
CHROME_CANDIDATES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def thai_long(day):
    return f"{day.day} {THAI_MONTHS[day.month - 1]} {day.year + BUDDHIST_OFFSET}"


def thai_short(day):
    return f"{day.day} {THAI_MONTHS_SHORT[day.month - 1]} {day.year + BUDDHIST_OFFSET}"


def report_meta(local_date, run_tag):
    start = datetime.strptime(local_date, "%Y-%m-%d")
    end = start + timedelta(days=1)
    run = datetime.strptime(run_tag, "%Y%m%d%H")
    return {
        "dateTh": thai_long(start),
        "startTh": f"07:00 น. {thai_short(start)}",
        "endTh": f"07:00 น. {thai_short(end)}",
        "run": f"{run:%H} UTC {thai_short(run)}",
    }


def airport_rows(points, airports):
    merged = airports.merge(points[["icao", "rain24_mm"]], on="icao", how="left")
    return [[r.region, r.icao, r.name_th, round(float(r.rain24_mm), 1), r.lat, r.lon, int(r.label_dx), int(r.label_dy)]
            for r in merged.itertuples()]


def project(lon, lat):
    return (lon - MAP_LON0) * MAP_K * MAP_COS, (MAP_LAT1 - lat) * MAP_K


def edge_taper(shape):
    rows = np.minimum(np.arange(shape[0]), np.arange(shape[0])[::-1]) / EDGE_FADE_PX
    cols = np.minimum(np.arange(shape[1]), np.arange(shape[1])[::-1]) / EDGE_FADE_PX
    return np.clip(np.outer(rows, np.ones(shape[1])), 0, 1) * np.clip(np.outer(np.ones(shape[0]), cols), 0, 1)


def rain_overlay(local_date, run_tag):
    with xr.open_dataset(GRID_DIR / f"wrfda_d02_24h_{local_date}_run{run_tag}.nc", engine="scipy") as ds:
        rain = ds["rain24_mm"].values.astype("float32")
        lons, lats = ds["x"].values, ds["y"].values
    field = Image.fromarray(np.flipud(rain), mode="F")
    field = field.resize((field.width * OVERLAY_UPSCALE, field.height * OVERLAY_UPSCALE), Image.BILINEAR)
    values = np.asarray(field)
    bounds = np.array([upper for upper, _ in OVERLAY_COLORS])
    palette = np.array([rgba for _, rgba in OVERLAY_COLORS], dtype="uint8")
    rgba = palette[np.searchsorted(bounds, values, side="right").clip(0, len(bounds) - 1)].copy()
    is_light = (values >= 0.1) & (values < 10.05)
    # light rain fades in with amount so widespread drizzle does not read as noise
    rgba[..., 3] = np.where(is_light, (LIGHT_ALPHA_MIN + (LIGHT_ALPHA_MAX - LIGHT_ALPHA_MIN) * values / 10.0), rgba[..., 3])
    rgba[..., 3] = (rgba[..., 3] * edge_taper(values.shape)).astype("uint8")
    image = Image.fromarray(rgba, mode="RGBA").filter(ImageFilter.GaussianBlur(1.2))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    dlon, dlat = float(lons[1] - lons[0]), float(lats[1] - lats[0])
    x0, y0 = project(float(lons[0]) - dlon / 2, float(lats[-1]) + dlat / 2)
    x1, y1 = project(float(lons[-1]) + dlon / 2, float(lats[0]) - dlat / 2)
    return {"href": "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode(),
            "x": round(x0, 2), "y": round(y0, 2), "w": round(x1 - x0, 2), "h": round(y1 - y0, 2)}


def write_html(local_date, rows, meta):
    html = (TEMPLATE.read_text(encoding="utf-8")
            .replace("__AIRPORTS__", json.dumps(rows, ensure_ascii=False))
            .replace("__REPORT__", json.dumps(meta, ensure_ascii=False)))
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"report_{local_date}.html"
    out.write_text(html, encoding="utf-8")
    return out


def find_chrome():
    found = [os.environ.get("CHROME_PATH")] + [shutil.which(c) or (c if Path(c).exists() else None)
                                               for c in CHROME_CANDIDATES]
    chrome = next((c for c in found if c), None)
    if chrome is None:
        raise RuntimeError("Chrome/Chromium not found; set CHROME_PATH")
    return chrome


def render_png(html_path):
    png = html_path.with_suffix(".png")
    sandbox = ["--no-sandbox"] if sys.platform.startswith("linux") else []
    cmd = [find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", *sandbox,
           f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}", f"--force-device-scale-factor={SCALE}",
           "--virtual-time-budget=8000", f"--screenshot={png}", html_path.resolve().as_uri()]
    subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    if not png.exists():
        raise RuntimeError(f"Chrome did not write {png}")
    return png


def write_preview(png):
    preview = png.with_name(png.stem + "_preview.jpg")
    with Image.open(png) as im:
        ratio = PREVIEW_WIDTH / im.width
        im.convert("RGB").resize((PREVIEW_WIDTH, round(im.height * ratio)), Image.LANCZOS).save(preview, quality=85)
    return preview


def main():
    parser = argparse.ArgumentParser(description="Build the 24 h airport rainfall report (HTML + PNG) from WRFDA")
    parser.add_argument("--date", default=datetime.now(BANGKOK).strftime("%Y-%m-%d"),
                        help="forecast date YYYY-MM-DD, period 07:00 that day to 07:00 next day (default: today)")
    parser.add_argument("--run", help="force model run YYYYMMDDHH (UTC)")
    parser.add_argument("--no-png", action="store_true", help="write HTML only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    airports = load_airports()
    run = datetime.strptime(args.run, "%Y%m%d%H").replace(tzinfo=timezone.utc) if args.run else None
    points = process_date(args.date, run, False, airports)
    run_tag = points["run"].iloc[0]
    meta = {**report_meta(args.date, run_tag), "overlay": rain_overlay(args.date, run_tag)}
    html = write_html(args.date, airport_rows(points, airports), meta)
    log.info("html -> %s (run %s)", html, meta["run"])
    if args.no_png:
        return
    png = render_png(html)
    preview = write_preview(png)
    log.info("png -> %s, preview -> %s", png.name, preview.name)


if __name__ == "__main__":
    main()
