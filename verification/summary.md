# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 9 days (2026-09-30 to 2026-10-08) · updated 2026-10-09 16:22 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 9 | 298 | 0.39 | 6.63 | 15.11 | 0.53 | 0.82 | 0.44 | 0.50 | 118 | 0.30 | 0.68 | 0.18 | 40 | 0.11 | 0.92 | 0.05 | 9 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 9 | 298 | -0.56 | 6.48 | 14.43 | 0.53 | 0.80 | 0.43 | 0.49 | 118 | 0.12 | 0.85 | 0.07 | 40 | 0.11 | 0.86 | 0.07 | 9 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 9 | 298 | 1.46 | 6.75 | 11.40 | 0.28 | 0.99 | 0.58 | 0.42 | 118 | 0.33 | 0.77 | 0.15 | 40 | 0.00 | 0.00 | 0.00 | 9 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 9 | 305 | -0.21 | 7.13 | 15.42 | 0.52 | 0.82 | 0.44 | 0.50 | 123 | 0.30 | 0.67 | 0.19 | 44 | 0.09 | 0.92 | 0.04 | 11 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 9 | 305 | -0.92 | 7.12 | 15.26 | 0.53 | 0.81 | 0.42 | 0.51 | 123 | 0.23 | 0.74 | 0.14 | 44 | 0.09 | 0.88 | 0.06 | 11 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 9 | 305 | 0.89 | 6.93 | 11.84 | 0.30 | 1.00 | 0.57 | 0.43 | 123 | 0.39 | 0.71 | 0.20 | 44 | 0.00 | 0.00 | 0.00 | 11 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 2.90 | 4.30 | 6.00 | 4.90 | 7.60 |
| ne_lower | 4.40 | 1.00 | 4.80 | 2.90 | 3.50 |
| ne_upper | 1.80 | 1.80 | 3.90 | 3.00 | 2.50 |
| north | 2.50 | 1.40 | 4.10 | 3.10 | 3.50 |
| southeast | 10.20 | 9.60 | 8.30 | 4.90 | 6.00 |
| southwest | 5.10 | 5.30 | 8.90 | 9.60 | 9.50 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
