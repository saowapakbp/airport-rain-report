# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 7 days (2026-09-30 to 2026-10-06) · updated 2026-10-07 14:23 ICT

Models at the nearest grid point. AWOS from verification/awos_manual.csv (T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 6 | 147 | 1.25 | 6.90 | 16.35 | 0.52 | 0.86 | 0.46 | 0.49 | 56 | 0.29 | 0.72 | 0.17 | 17 | 0.00 | 1.00 | 0.00 | 4 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 6 | 147 | -0.19 | 5.67 | 12.88 | 0.51 | 0.80 | 0.48 | 0.46 | 56 | 0.18 | 0.81 | 0.10 | 17 | 0.00 | 1.00 | 0.00 | 4 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 6 | 147 | 2.30 | 6.49 | 9.58 | 0.24 | 1.00 | 0.62 | 0.38 | 56 | 0.35 | 0.75 | 0.17 | 17 | 0.00 | 0.00 | 0.00 | 4 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 7 | 237 | 0.26 | 7.47 | 15.62 | 0.49 | 0.81 | 0.42 | 0.51 | 107 | 0.28 | 0.69 | 0.17 | 36 | 0.14 | 0.91 | 0.06 | 7 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 7 | 237 | -0.41 | 7.26 | 14.18 | 0.50 | 0.79 | 0.40 | 0.52 | 107 | 0.25 | 0.74 | 0.15 | 36 | 0.14 | 0.86 | 0.08 | 7 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 7 | 237 | 1.42 | 6.95 | 10.63 | 0.30 | 1.00 | 0.54 | 0.46 | 107 | 0.39 | 0.71 | 0.20 | 36 | 0.00 | 0.00 | 0.00 | 7 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 3.60 | 5.00 | 6.70 | 5.50 | 9.20 |
| ne_lower | 5.60 | 1.30 | 6.10 | 1.60 | 4.50 |
| ne_upper | 2.40 | 2.40 | 5.00 | 3.90 | 3.20 |
| north | 3.20 | 1.80 | 5.00 | 2.70 | 3.70 |
| southeast | 9.70 | 9.80 | 7.60 | 2.40 | 4.40 |
| southwest | 5.60 | 6.40 | 9.00 | 9.30 | 8.80 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
