# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 16 days (2026-09-30 to 2026-10-16) · updated 2026-10-17 14:09 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 16 | 536 | 0.44 | 6.13 | 13.47 | 0.53 | 0.82 | 0.42 | 0.51 | 220 | 0.33 | 0.67 | 0.20 | 72 | 0.07 | 0.94 | 0.03 | 14 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 16 | 536 | 0.46 | 6.36 | 13.75 | 0.54 | 0.79 | 0.42 | 0.50 | 220 | 0.25 | 0.75 | 0.14 | 72 | 0.14 | 0.90 | 0.06 | 14 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 16 | 536 | 1.99 | 6.56 | 10.53 | 0.26 | 0.99 | 0.57 | 0.42 | 220 | 0.39 | 0.76 | 0.17 | 72 | 0.00 | 0.00 | 0.00 | 14 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 16 | 543 | -0.70 | 6.90 | 16.67 | 0.52 | 0.83 | 0.42 | 0.52 | 223 | 0.36 | 0.61 | 0.23 | 80 | 0.05 | 0.94 | 0.03 | 21 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 16 | 543 | -0.56 | 7.21 | 17.12 | 0.54 | 0.83 | 0.40 | 0.53 | 223 | 0.34 | 0.65 | 0.21 | 80 | 0.14 | 0.86 | 0.08 | 21 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 16 | 543 | 0.86 | 7.36 | 15.07 | 0.27 | 1.00 | 0.57 | 0.43 | 223 | 0.44 | 0.70 | 0.21 | 80 | 0.00 | 0.00 | 0.00 | 21 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 3.60 | 8.10 | 8.40 | 3.50 | 10.50 |
| ne_lower | 3.30 | 1.50 | 5.20 | 2.40 | 2.80 |
| ne_upper | 1.90 | 1.40 | 3.40 | 1.70 | 1.50 |
| north | 1.90 | 1.80 | 3.90 | 2.40 | 2.60 |
| southeast | 9.00 | 8.30 | 8.60 | 6.20 | 7.60 |
| southwest | 7.30 | 9.20 | 9.20 | 9.30 | 10.20 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
