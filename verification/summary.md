# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 15 days (2026-09-30 to 2026-10-15) · updated 2026-10-16 14:25 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 15 | 500 | 0.54 | 6.40 | 13.83 | 0.52 | 0.82 | 0.42 | 0.51 | 210 | 0.33 | 0.68 | 0.19 | 70 | 0.08 | 0.94 | 0.03 | 13 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 15 | 500 | 0.46 | 6.55 | 14.00 | 0.52 | 0.79 | 0.42 | 0.50 | 210 | 0.24 | 0.76 | 0.14 | 70 | 0.15 | 0.89 | 0.07 | 13 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 15 | 500 | 2.05 | 6.76 | 10.75 | 0.26 | 1.00 | 0.56 | 0.43 | 210 | 0.39 | 0.76 | 0.17 | 70 | 0.00 | 0.00 | 0.00 | 13 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 15 | 509 | -0.45 | 7.05 | 16.82 | 0.51 | 0.83 | 0.42 | 0.52 | 213 | 0.36 | 0.62 | 0.23 | 77 | 0.06 | 0.94 | 0.03 | 18 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 15 | 509 | -0.41 | 7.37 | 17.37 | 0.53 | 0.82 | 0.40 | 0.53 | 213 | 0.32 | 0.66 | 0.20 | 77 | 0.17 | 0.85 | 0.09 | 18 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 15 | 509 | 1.04 | 7.41 | 15.13 | 0.28 | 1.00 | 0.56 | 0.44 | 213 | 0.44 | 0.70 | 0.22 | 77 | 0.00 | 0.00 | 0.00 | 18 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 3.70 | 7.80 | 8.40 | 3.60 | 11.00 |
| ne_lower | 3.50 | 1.60 | 5.50 | 2.50 | 2.90 |
| ne_upper | 2.00 | 1.50 | 3.70 | 1.80 | 1.60 |
| north | 2.10 | 1.90 | 4.00 | 2.60 | 2.80 |
| southeast | 9.50 | 8.80 | 8.80 | 6.60 | 8.10 |
| southwest | 7.40 | 9.10 | 9.30 | 8.80 | 8.10 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
