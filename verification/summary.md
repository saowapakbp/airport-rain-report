# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 5 days (2026-09-30 to 2026-10-04) · updated 2026-10-05 14:15 ICT

Models at the nearest grid point. AWOS from verification/awos_manual.csv (T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 2 | 43 | 2.01 | 3.83 | 10.63 | 0.63 | 0.92 | 0.52 | 0.46 | 12 | 0.50 | 0.75 | 0.20 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 2 | 43 | 1.29 | 3.74 | 13.01 | 0.60 | 0.75 | 0.55 | 0.39 | 12 | 0.00 | 1.00 | 0.00 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 2 | 43 | 3.29 | 4.64 | 7.17 | 0.21 | 1.00 | 0.72 | 0.28 | 12 | 0.50 | 0.80 | 0.17 | 2 | 0.00 | 0.00 | 0.00 | 0 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 5 | 169 | 0.16 | 4.99 | 11.00 | 0.53 | 0.77 | 0.47 | 0.46 | 66 | 0.07 | 0.93 | 0.04 | 14 | 0.00 | 1.00 | 0.00 | 2 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 5 | 169 | 0.80 | 5.64 | 12.88 | 0.54 | 0.79 | 0.45 | 0.48 | 66 | 0.14 | 0.89 | 0.06 | 14 | 0.00 | 1.00 | 0.00 | 2 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 5 | 169 | 2.21 | 5.26 | 8.04 | 0.30 | 1.00 | 0.60 | 0.40 | 66 | 0.43 | 0.73 | 0.20 | 14 | 0.00 | 0.00 | 0.00 | 2 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 1.70 | 2.10 | 4.10 | 0.00 | 3.70 |
| ne_lower | 2.30 | 1.40 | 5.40 | 0.40 | 5.90 |
| ne_upper | 0.90 | 2.20 | 4.50 | 0.00 | 3.40 |
| north | 0.90 | 0.30 | 2.80 | 0.30 | 0.80 |
| southeast | 6.90 | 9.80 | 6.90 | 3.40 | 1.70 |
| southwest | 5.90 | 5.90 | 9.00 | 9.40 | 7.20 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
