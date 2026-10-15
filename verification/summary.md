# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 14 days (2026-09-30 to 2026-10-14) · updated 2026-10-15 14:48 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 14 | 463 | 0.68 | 6.67 | 14.22 | 0.50 | 0.83 | 0.44 | 0.51 | 194 | 0.34 | 0.67 | 0.20 | 67 | 0.08 | 0.94 | 0.03 | 12 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 14 | 463 | 0.47 | 6.76 | 14.36 | 0.52 | 0.80 | 0.42 | 0.50 | 194 | 0.24 | 0.76 | 0.14 | 67 | 0.17 | 0.89 | 0.07 | 12 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 14 | 463 | 2.07 | 6.88 | 10.88 | 0.25 | 0.99 | 0.57 | 0.43 | 194 | 0.40 | 0.75 | 0.18 | 67 | 0.00 | 0.00 | 0.00 | 12 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 14 | 475 | -0.41 | 7.42 | 17.37 | 0.49 | 0.84 | 0.43 | 0.52 | 200 | 0.37 | 0.62 | 0.23 | 75 | 0.06 | 0.94 | 0.03 | 18 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 14 | 475 | -0.52 | 7.67 | 17.89 | 0.52 | 0.83 | 0.40 | 0.53 | 200 | 0.32 | 0.66 | 0.20 | 75 | 0.17 | 0.84 | 0.09 | 18 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 14 | 475 | 0.99 | 7.68 | 15.60 | 0.28 | 1.00 | 0.56 | 0.44 | 200 | 0.45 | 0.70 | 0.22 | 75 | 0.00 | 0.00 | 0.00 | 18 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 4.00 | 7.90 | 8.70 | 3.90 | 11.80 |
| ne_lower | 3.80 | 1.70 | 5.70 | 2.70 | 3.10 |
| ne_upper | 2.10 | 1.60 | 3.90 | 2.00 | 1.70 |
| north | 2.20 | 2.00 | 4.10 | 2.30 | 2.70 |
| southeast | 10.20 | 9.30 | 9.00 | 7.10 | 8.60 |
| southwest | 7.70 | 8.90 | 9.70 | 9.00 | 8.30 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
