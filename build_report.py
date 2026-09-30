import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from PIL import Image

from common import HERE, load_airports
from fetch_wrfda_24h import process_date

log = logging.getLogger("report")

TEMPLATE = HERE / "report_template.html"
REPORT_DIR = HERE / "reports"
BANGKOK = timezone(timedelta(hours=7))
THAI_MONTHS = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
               "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
THAI_MONTHS_SHORT = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
                     "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
BUDDHIST_OFFSET = 543
VIEWPORT = (1560, 1100)
SCALE = 1.5
PREVIEW_WIDTH = 1040
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
    meta = report_meta(args.date, points["run"].iloc[0])
    html = write_html(args.date, airport_rows(points, airports), meta)
    log.info("html -> %s (run %s)", html, meta["run"])
    if args.no_png:
        return
    png = render_png(html)
    preview = write_preview(png)
    log.info("png -> %s, preview -> %s", png.name, preview.name)


if __name__ == "__main__":
    main()
