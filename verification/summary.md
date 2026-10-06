# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 6 days (2026-09-30 to 2026-10-05) · updated 2026-10-06 16:13 ICT

Models at the nearest grid point. AWOS from verification/awos_manual.csv (T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 2 | 43 | 2.01 | 3.83 | 10.63 | 0.63 | 0.92 | 0.52 | 0.46 | 12 | 0.50 | 0.75 | 0.20 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 2 | 43 | 1.29 | 3.74 | 13.01 | 0.60 | 0.75 | 0.55 | 0.39 | 12 | 0.00 | 1.00 | 0.00 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 2 | 43 | 3.29 | 4.64 | 7.17 | 0.21 | 1.00 | 0.72 | 0.28 | 12 | 0.50 | 0.80 | 0.17 | 2 | 0.00 | 0.00 | 0.00 | 0 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 6 | 203 | 0.96 | 7.22 | 15.68 | 0.49 | 0.81 | 0.44 | 0.49 | 88 | 0.27 | 0.74 | 0.15 | 26 | 0.20 | 0.90 | 0.07 | 5 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 6 | 203 | 0.10 | 6.64 | 13.51 | 0.51 | 0.82 | 0.41 | 0.52 | 88 | 0.23 | 0.79 | 0.12 | 26 | 0.20 | 0.83 | 0.10 | 5 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 6 | 203 | 1.79 | 6.58 | 9.97 | 0.28 | 1.00 | 0.56 | 0.44 | 88 | 0.35 | 0.75 | 0.17 | 26 | 0.00 | 0.00 | 0.00 | 5 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 4.00 | 3.20 | 5.60 | 0.00 | 8.70 |
| ne_lower | 6.50 | 1.50 | 6.50 | 0.40 | 5.00 |
| ne_upper | 2.80 | 2.80 | 5.80 | 0.00 | 3.70 |
| north | 2.20 | 1.80 | 4.50 | 0.30 | 2.20 |
| southeast | 10.40 | 9.90 | 6.80 | 3.40 | 3.90 |
| southwest | 5.00 | 5.30 | 8.50 | 9.40 | 6.70 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
