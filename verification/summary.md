# Verification: WRFDA vs ECMWF IFS vs SYNOP

24 h rainfall 07:00–07:00 local at 34 airports · 2 days (2026-09-30 to 2026-10-01) · updated 2026-10-02 15:42 ICT

Truth: GTS SYNOP 24 h rain at 00 UTC (group 333 7RRRR). Both models use the run the daily report used (12 UTC previous day, 00 UTC fallback), nearest grid point. ECMWF open data (CC BY 4.0).

## Scores

| ชุดข้อมูล | แบบจำลอง | n | bias | MAE | RMSE | r | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ทุกสนามบิน | WRFDA d02 (3 km) | 68 | 1.07 | 4.21 | 10.16 | -0.01 | 0.59 | 0.75 | 0.55 | 0.39 | 20 | 0.00 | 1.00 | 0.00 | 4 | 0.00 | 1.00 | 0.00 | 0 |
| ทุกสนามบิน | ECMWF IFS (0.25°) | 68 | 3.00 | 4.65 | 7.29 | 0.24 | 0.24 | 1.00 | 0.70 | 0.30 | 20 | 0.50 | 0.78 | 0.18 | 4 | 0.00 | 0.00 | 0.00 | 0 |
| สถานีห่าง ≤ 15 กม. | WRFDA d02 (3 km) | 56 | 0.40 | 3.49 | 8.25 | 0.01 | 0.57 | 0.71 | 0.62 | 0.33 | 14 | 0.00 | 1.00 | 0.00 | 3 | 0.00 | 1.00 | 0.00 | 0 |
| สถานีห่าง ≤ 15 กม. | ECMWF IFS (0.25°) | 56 | 2.35 | 4.01 | 6.37 | 0.34 | 0.21 | 1.00 | 0.74 | 0.26 | 14 | 0.67 | 0.71 | 0.25 | 3 | 0.00 | 0.00 | 0.00 | 0 |

## Mean 24 h rain by region (mm)

| region | wrfda_mm | ifs_mm | obs24_mm |
|---|---|---|---|
| central | 1.90 | 4.10 | 2.40 |
| ne_lower | 0.00 | 4.60 | 5.20 |
| ne_upper | 0.50 | 3.00 | 0.00 |
| north | 2.00 | 1.50 | 0.10 |
| southeast | 8.00 | 8.20 | 0.90 |
| southwest | 2.20 | 10.20 | 7.00 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. One day of scores is noise; read them after a month or more.
