# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 11 days (2026-09-30 to 2026-10-10) · updated 2026-10-11 16:09 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 11 | 364 | -0.09 | 6.70 | 15.48 | 0.52 | 0.82 | 0.43 | 0.51 | 148 | 0.31 | 0.65 | 0.20 | 52 | 0.10 | 0.93 | 0.04 | 10 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 11 | 364 | -0.65 | 6.71 | 15.36 | 0.51 | 0.79 | 0.43 | 0.49 | 148 | 0.15 | 0.82 | 0.09 | 52 | 0.10 | 0.90 | 0.05 | 10 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 11 | 364 | 1.34 | 6.91 | 12.36 | 0.27 | 0.99 | 0.57 | 0.42 | 148 | 0.38 | 0.74 | 0.19 | 52 | 0.00 | 0.00 | 0.00 | 10 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 11 | 373 | -1.12 | 7.47 | 18.46 | 0.51 | 0.83 | 0.43 | 0.51 | 151 | 0.31 | 0.63 | 0.20 | 58 | 0.07 | 0.93 | 0.04 | 14 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 11 | 373 | -1.50 | 7.62 | 18.66 | 0.52 | 0.82 | 0.42 | 0.51 | 151 | 0.24 | 0.71 | 0.15 | 58 | 0.14 | 0.82 | 0.09 | 14 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 11 | 373 | 0.31 | 7.68 | 16.70 | 0.29 | 1.00 | 0.57 | 0.43 | 151 | 0.41 | 0.70 | 0.21 | 58 | 0.00 | 0.00 | 0.00 | 14 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 3.00 | 5.90 | 7.20 | 4.10 | 12.60 |
| ne_lower | 3.70 | 1.30 | 5.20 | 3.40 | 3.70 |
| ne_upper | 2.30 | 2.00 | 4.10 | 2.50 | 2.10 |
| north | 2.20 | 1.60 | 4.00 | 2.80 | 3.40 |
| southeast | 9.80 | 8.70 | 8.40 | 6.40 | 7.40 |
| southwest | 5.10 | 6.10 | 8.60 | 10.20 | 9.50 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
