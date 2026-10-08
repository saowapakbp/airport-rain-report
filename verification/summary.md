# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 8 days (2026-09-30 to 2026-10-07) · updated 2026-10-08 22:22 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 8 | 264 | 0.50 | 7.00 | 15.40 | 0.52 | 0.83 | 0.43 | 0.51 | 110 | 0.29 | 0.68 | 0.18 | 38 | 0.12 | 0.92 | 0.05 | 8 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 8 | 264 | -0.46 | 6.79 | 14.40 | 0.50 | 0.80 | 0.44 | 0.49 | 110 | 0.13 | 0.85 | 0.08 | 38 | 0.12 | 0.86 | 0.07 | 8 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 8 | 264 | 1.57 | 6.92 | 10.93 | 0.27 | 0.99 | 0.57 | 0.43 | 110 | 0.34 | 0.75 | 0.17 | 38 | 0.00 | 0.00 | 0.00 | 8 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 8 | 271 | -0.15 | 7.53 | 15.72 | 0.50 | 0.81 | 0.42 | 0.51 | 118 | 0.29 | 0.67 | 0.18 | 42 | 0.10 | 0.92 | 0.05 | 10 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 8 | 271 | -0.84 | 7.47 | 15.32 | 0.50 | 0.81 | 0.41 | 0.52 | 118 | 0.24 | 0.73 | 0.14 | 42 | 0.10 | 0.88 | 0.06 | 10 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 8 | 271 | 0.94 | 7.10 | 11.45 | 0.30 | 1.00 | 0.54 | 0.46 | 118 | 0.40 | 0.69 | 0.21 | 42 | 0.00 | 0.00 | 0.00 | 10 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 3.10 | 4.80 | 6.40 | 5.50 | 8.60 |
| ne_lower | 4.90 | 1.10 | 5.40 | 3.30 | 3.90 |
| ne_upper | 2.10 | 2.10 | 4.40 | 3.30 | 2.80 |
| north | 2.80 | 1.60 | 4.60 | 3.50 | 3.90 |
| southeast | 10.30 | 10.00 | 8.00 | 3.80 | 5.20 |
| southwest | 5.70 | 5.80 | 9.30 | 10.70 | 10.50 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
