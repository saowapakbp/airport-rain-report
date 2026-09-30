# Airport 24 h rainfall report

Daily 24-hour accumulated rainfall forecast (07:00-07:00 local) for 34 Thai airports from the TMD WRFDA 3 km Domain 2 model.
GitHub Actions builds `reports/report_YYYY-MM-DD.png` at 06:30 (Asia/Bangkok) and pushes it to LINE.

- `build_report.py` - download WRFDA, sum 24 h at the nearest grid point, fill `report_template.html`, render PNG
- `notify_line.py` - push the image to LINE (secrets `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_USER_ID`)
- `fetch_synop_24h.py` - GTS SYNOP 24 h observations for verification
