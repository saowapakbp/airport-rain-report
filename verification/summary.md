# Verification: WRFDA vs ECMWF IFS vs SYNOP

24 h rainfall 07:00–07:00 local at 34 airports · 1 days (2026-09-30 to 2026-09-30) · updated 2026-10-01 08:52 ICT

Truth: GTS SYNOP 24 h rain at 00 UTC (group 333 7RRRR). Both models use the run the daily report used (12 UTC previous day, 00 UTC fallback), nearest grid point. ECMWF open data (CC BY 4.0).

## Scores

| ชุดข้อมูล | แบบจำลอง | n | bias | MAE | RMSE | r | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ทุกสนามบิน | WRFDA d02 (3 km) | 34 | 2.04 | 6.78 | 13.83 | -0.07 | 0.53 | 0.77 | 0.47 | 0.45 | 13 | 0.00 | 1.00 | 0.00 | 3 | 0.00 | 1.00 | 0.00 | 0 |
| ทุกสนามบิน | ECMWF IFS (0.25°) | 34 | 3.36 | 6.02 | 9.26 | 0.14 | 0.24 | 1.00 | 0.62 | 0.38 | 13 | 0.33 | 0.86 | 0.11 | 3 | 0.00 | 0.00 | 0.00 | 0 |
| สถานีห่าง ≤ 15 กม. | WRFDA d02 (3 km) | 28 | 1.13 | 5.45 | 10.97 | -0.05 | 0.54 | 0.78 | 0.53 | 0.41 | 9 | 0.00 | 1.00 | 0.00 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| สถานีห่าง ≤ 15 กม. | ECMWF IFS (0.25°) | 28 | 2.68 | 5.20 | 8.02 | 0.26 | 0.21 | 1.00 | 0.68 | 0.32 | 9 | 0.50 | 0.80 | 0.17 | 2 | 0.00 | 0.00 | 0.00 | 0 |

## Mean 24 h rain by region (mm)

| region | wrfda_mm | ifs_mm | obs24_mm |
|---|---|---|---|
| central | 1.10 | 2.70 | 4.70 |
| ne_lower | 0.00 | 5.80 | 9.80 |
| ne_upper | 1.00 | 1.90 | 0.00 |
| north | 4.00 | 2.50 | 0.20 |
| southeast | 13.80 | 12.20 | 1.50 |
| southwest | 1.30 | 11.20 | 6.60 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. One day of scores is noise; read them after a month or more.
