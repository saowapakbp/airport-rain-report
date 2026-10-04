# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 4 days (2026-09-30 to 2026-10-03) · updated 2026-10-04 15:38 ICT

Models at the nearest grid point. AWOS from verification/awos_manual.csv (T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 2 | 43 | 2.01 | 3.83 | 10.63 | 0.63 | 0.92 | 0.52 | 0.46 | 12 | 0.50 | 0.75 | 0.20 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 2 | 43 | 1.29 | 3.74 | 13.01 | 0.60 | 0.75 | 0.55 | 0.39 | 12 | 0.00 | 1.00 | 0.00 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 2 | 43 | 3.29 | 4.64 | 7.17 | 0.21 | 1.00 | 0.72 | 0.28 | 12 | 0.50 | 0.80 | 0.17 | 2 | 0.00 | 0.00 | 0.00 | 0 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 4 | 136 | 0.73 | 4.17 | 10.16 | 0.58 | 0.84 | 0.51 | 0.45 | 44 | 0.12 | 0.91 | 0.06 | 8 | 0.00 | 1.00 | 0.00 | 1 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 4 | 136 | 1.59 | 5.04 | 12.60 | 0.57 | 0.82 | 0.51 | 0.44 | 44 | 0.12 | 0.92 | 0.05 | 8 | 0.00 | 1.00 | 0.00 | 1 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 4 | 136 | 2.83 | 4.75 | 7.18 | 0.26 | 1.00 | 0.67 | 0.33 | 44 | 0.62 | 0.71 | 0.25 | 8 | 0.00 | 0.00 | 0.00 | 1 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 2.10 | 1.00 | 4.70 | 0.00 | 2.50 |
| ne_lower | 1.30 | 1.30 | 4.40 | 0.40 | 3.00 |
| ne_upper | 0.50 | 2.10 | 4.00 | 0.00 | 0.40 |
| north | 1.10 | 0.40 | 1.70 | 0.30 | 0.40 |
| southeast | 5.90 | 9.80 | 7.60 | 3.40 | 1.80 |
| southwest | 7.10 | 7.20 | 10.40 | 9.40 | 8.60 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
