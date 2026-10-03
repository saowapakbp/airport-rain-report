# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 3 days (2026-09-30 to 2026-10-02) · updated 2026-10-03 13:41 ICT

Models at the nearest grid point. AWOS from verification/awos_manual.csv (T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 2 | 43 | 2.01 | 3.83 | 10.63 | 0.63 | 0.92 | 0.52 | 0.46 | 12 | 0.50 | 0.75 | 0.20 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 2 | 43 | 1.29 | 3.74 | 13.01 | 0.60 | 0.75 | 0.55 | 0.39 | 12 | 0.00 | 1.00 | 0.00 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 2 | 43 | 3.29 | 4.64 | 7.17 | 0.21 | 1.00 | 0.72 | 0.28 | 12 | 0.50 | 0.80 | 0.17 | 2 | 0.00 | 0.00 | 0.00 | 0 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 3 | 102 | 0.68 | 3.71 | 9.36 | 0.61 | 0.83 | 0.54 | 0.42 | 29 | 0.20 | 0.86 | 0.09 | 5 | 0.00 | 1.00 | 0.00 | 1 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 3 | 102 | 1.75 | 4.69 | 12.93 | 0.62 | 0.79 | 0.51 | 0.43 | 29 | 0.20 | 0.89 | 0.08 | 5 | 0.00 | 1.00 | 0.00 | 1 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 3 | 102 | 2.79 | 4.61 | 7.36 | 0.22 | 1.00 | 0.71 | 0.29 | 29 | 0.60 | 0.77 | 0.20 | 5 | 0.00 | 0.00 | 0.00 | 1 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 2.00 | 1.00 | 4.30 | 0.00 | 1.80 |
| ne_lower | 0.60 | 1.10 | 4.70 | 0.40 | 4.00 |
| ne_upper | 0.60 | 0.60 | 3.80 | 0.00 | 0.00 |
| north | 1.40 | 0.30 | 1.30 | 0.30 | 0.30 |
| southeast | 6.30 | 10.30 | 7.50 | 3.40 | 0.60 |
| southwest | 3.40 | 7.30 | 9.40 | 9.40 | 9.30 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
