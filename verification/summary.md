# Verification: WRFDA 12/18 UTC and ECMWF IFS vs AWOS and SYNOP

24 h rainfall 07:00–07:00 ICT at 34 airports · 2 days (2026-09-30 to 2026-10-01) · updated 2026-10-02 23:56 ICT

Models at the nearest grid point. AWOS from verification/awos_manual.csv (T = 0.05 mm, missing/fault excluded); SYNOP 24 h rain at 00 UTC (group 333 7RRRR). ECMWF open data (CC BY 4.0).

## Scores

| truth | model | days | n | bias | MAE | RMSE | cat_match | POD≥0.1 | FAR≥0.1 | CSI≥0.1 | obs≥0.1 | POD≥10 | FAR≥10 | CSI≥10 | obs≥10 | POD≥35.1 | FAR≥35.1 | CSI≥35.1 | obs≥35.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AWOS (airport) | WRFDA 12 UTC (19:00 ICT) | 2 | 43 | 2.01 | 3.83 | 10.63 | 0.63 | 0.92 | 0.52 | 0.46 | 12 | 0.50 | 0.75 | 0.20 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | WRFDA 18 UTC (01:00 ICT) | 2 | 43 | 1.29 | 3.74 | 13.01 | 0.60 | 0.75 | 0.55 | 0.39 | 12 | 0.00 | 1.00 | 0.00 | 2 | 0.00 | 1.00 | 0.00 | 0 |
| AWOS (airport) | ECMWF IFS 12 UTC (0.25°) | 2 | 43 | 3.29 | 4.64 | 7.17 | 0.21 | 1.00 | 0.72 | 0.28 | 12 | 0.50 | 0.80 | 0.17 | 2 | 0.00 | 0.00 | 0.00 | 0 |
| SYNOP (nearest station) | WRFDA 12 UTC (19:00 ICT) | 2 | 68 | 1.60 | 4.75 | 10.99 | 0.54 | 0.80 | 0.57 | 0.39 | 20 | 0.00 | 1.00 | 0.00 | 4 | 0.00 | 1.00 | 0.00 | 0 |
| SYNOP (nearest station) | WRFDA 18 UTC (01:00 ICT) | 2 | 68 | 1.80 | 4.73 | 13.48 | 0.60 | 0.80 | 0.52 | 0.43 | 20 | 0.00 | 1.00 | 0.00 | 4 | 0.00 | 1.00 | 0.00 | 0 |
| SYNOP (nearest station) | ECMWF IFS 12 UTC (0.25°) | 2 | 68 | 2.90 | 4.59 | 7.27 | 0.24 | 1.00 | 0.70 | 0.30 | 20 | 0.50 | 0.78 | 0.18 | 4 | 0.00 | 0.00 | 0.00 | 0 |

## Mean 24 h rain by region (mm)

| region | wrfda12_mm | wrfda18_mm | ifs12_mm | awos_mm | obs24_mm |
|---|---|---|---|---|---|
| central | 3.00 | 1.40 | 4.30 | 0.00 | 2.40 |
| ne_lower | 0.60 | 1.50 | 4.90 | 0.40 | 5.20 |
| ne_upper | 0.60 | 0.00 | 3.20 | 0.00 | 0.00 |
| north | 2.00 | 0.50 | 1.40 | 0.30 | 0.10 |
| southeast | 9.10 | 12.90 | 7.80 | 3.40 | 0.90 |
| southwest | 2.60 | 1.80 | 9.50 | 9.40 | 7.00 |

Categories: none < 0.1, light < 10.05, mod < 35.05, heavy < 90.05 mm. A few days of scores are noise; read them after a month or more.
