# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 13 days (2026-09-30 to 2026-10-13) · updated 2026-10-14 14:53 ICT

Models at the nearest grid point. AWOS from the aeromet2 daily rainfall API (verification/awos_history.csv, T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 13 | 431 | 0.43 | 6.75 | 14.51 | 0.51 | 0.83 | 0.44 | 0.50 | 177 | 0.33 | 0.65 | 0.21 | 63 | 0.08 | 0.94 | 0.04 | 12 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 13 | 431 | 0.29 | 6.93 | 14.67 | 0.51 | 0.81 | 0.43 | 0.50 | 177 | 0.21 | 0.78 | 0.12 | 63 | 0.17 | 0.88 | 0.08 | 12 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 13 | 431 | 2.00 | 6.98 | 11.11 | 0.26 | 0.99 | 0.57 | 0.43 | 177 | 0.43 | 0.74 | 0.20 | 63 | 0.00 | 0.00 | 0.00 | 12 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 13 | 441 | -0.70 | 7.60 | 17.83 | 0.50 | 0.85 | 0.43 | 0.52 | 182 | 0.34 | 0.62 | 0.22 | 70 | 0.06 | 0.94 | 0.03 | 18 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 13 | 441 | -0.72 | 7.89 | 18.37 | 0.52 | 0.84 | 0.42 | 0.52 | 182 | 0.29 | 0.69 | 0.18 | 70 | 0.17 | 0.82 | 0.09 | 18 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 13 | 441 | 0.87 | 7.85 | 16.06 | 0.28 | 1.00 | 0.57 | 0.43 | 182 | 0.47 | 0.69 | 0.23 | 70 | 0.00 | 0.00 | 0.00 | 18 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 3.80 | 8.20 | 8.70 | 4.10 | 11.90 |
| ne_lower | 3.80 | 1.80 | 5.60 | 2.90 | 3.30 |
| ne_upper | 2.30 | 1.70 | 4.00 | 2.10 | 1.80 |
| north | 2.10 | 2.10 | 4.10 | 2.40 | 2.90 |
| southeast | 9.70 | 8.90 | 9.20 | 7.00 | 8.70 |
| southwest | 7.60 | 8.60 | 9.60 | 9.40 | 8.70 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
