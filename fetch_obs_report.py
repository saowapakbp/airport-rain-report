import argparse
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import urllib3
from PIL import Image
from playwright.sync_api import sync_playwright


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = logging.getLogger("obs")

PAGE = "https://aeromet2.tmd.go.th/reports/daily-rainfall?date={date}"
API = "https://aeromet2.tmd.go.th/api/daily-obs/rainfall-report"
OUT_DIR = Path(__file__).resolve().parent / "reports" / "obs"
BANGKOK = timezone(timedelta(hours=7))
SCALE = 2
PREVIEW_WIDTH = 760
# the report card on the page is an A4-sized <article>; this text only appears once its data has rendered
REPORT_SELECTOR = "article:has-text('Airport Daily Rainfall Report')"
READY_TEXT = "ประจำวันที่"


def published(local_date):
    body = requests.get(API, params={"date": local_date}, timeout=30, verify=False).json()
    if "error" in body:
        log.info("%s not available: %s", local_date, body["error"].get("code"))
        return False
    return True


def launch(p):
    # use the runner's Google Chrome when present, otherwise the bundled Chromium
    try:
        return p.chromium.launch(channel="chrome")
    except Exception:
        return p.chromium.launch()


def capture(local_date):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png = OUT_DIR / f"obs_{local_date}.png"
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1280, "height": 1600}, device_scale_factor=SCALE, ignore_https_errors=True)
        page.goto(PAGE.format(date=local_date), wait_until="load", timeout=90_000)
        card = page.locator(REPORT_SELECTOR).first
        card.wait_for(state="visible", timeout=60_000)
        page.wait_for_function("t => document.body.innerText.includes(t)", arg=READY_TEXT, timeout=60_000)
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1500)
        card.screenshot(path=str(png))
        browser.close()
    preview = png.with_name(png.stem + "_preview.jpg")
    with Image.open(png) as im:
        im.convert("RGB").resize((PREVIEW_WIDTH, round(im.height * PREVIEW_WIDTH / im.width)), Image.LANCZOS).save(preview, quality=85)
    log.info("%s -> %s, %s", local_date, png.name, preview.name)
    return png


def main():
    yesterday = (datetime.now(BANGKOK) - timedelta(days=1)).strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description="Capture the aeromet2 daily AWOS rainfall report as PNG")
    parser.add_argument("--date", default=yesterday, help="observation period start YYYY-MM-DD (default: yesterday ICT)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not published(args.date):
        raise SystemExit(f"report for {args.date} not published yet")
    capture(args.date)


if __name__ == "__main__":
    main()
