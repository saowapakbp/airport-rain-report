# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 10 days (2026-09-30 to 2026-10-09) · updated 2026-10-10 15:44 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 10 | 332 | 0.21 | 6.37 | 14.63 | 0.54 | 0.81 | 0.44 | 0.49 | 128 | 0.29 | 0.67 | 0.18 | 45 | 0.11 | 0.92 | 0.05 | 9 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 10 | 332 | -0.61 | 6.20 | 14.01 | 0.53 | 0.77 | 0.45 | 0.48 | 128 | 0.13 | 0.83 | 0.08 | 45 | 0.11 | 0.88 | 0.06 | 9 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 10 | 332 | 1.28 | 6.47 | 11.05 | 0.26 | 0.99 | 0.59 | 0.40 | 128 | 0.31 | 0.77 | 0.15 | 45 | 0.00 | 0.00 | 0.00 | 9 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 10 | 339 | -1.16 | 7.42 | 18.89 | 0.54 | 0.82 | 0.43 | 0.50 | 134 | 0.31 | 0.63 | 0.20 | 49 | 0.08 | 0.92 | 0.04 | 13 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 10 | 339 | -1.77 | 7.38 | 18.90 | 0.54 | 0.81 | 0.42 | 0.51 | 134 | 0.24 | 0.70 | 0.16 | 49 | 0.15 | 0.78 | 0.10 | 13 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 10 | 339 | -0.07 | 7.49 | 17.08 | 0.28 | 1.00 | 0.58 | 0.42 | 134 | 0.37 | 0.72 | 0.19 | 49 | 0.00 | 0.00 | 0.00 | 13 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 2.90 | 3.90 | 5.60 | 4.40 | 13.90 |
| ne_lower | 3.90 | 1.00 | 4.50 | 2.60 | 3.10 |
| ne_upper | 1.70 | 1.70 | 3.60 | 2.70 | 2.30 |
| north | 2.20 | 1.30 | 3.80 | 2.80 | 3.10 |
| southeast | 9.70 | 9.20 | 8.10 | 4.90 | 7.10 |
| southwest | 5.00 | 5.50 | 8.70 | 10.50 | 9.70 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
