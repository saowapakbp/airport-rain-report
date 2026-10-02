# P(24 h rain ≥ 10 mm) — WRFDA 12 UTC, cross-validated against SYNOP

1701 airport-days, 61 days (2026-08-02 to 2026-10-01), 369 events (22%). 5-fold CV grouped by ISO week. Updated 2026-10-03 00:47 ICT.

| method | Brier | BSS vs climatology | AUC | mean prob | observed rate |
|---|---|---|---|---|---|
| logistic | 0.15 | 0.11 | 0.73 | 0.21 | 0.22 |
| random_forest | 0.15 | 0.10 | 0.71 | 0.22 | 0.22 |
| xgboost | 0.16 | 0.08 | 0.71 | 0.21 | 0.22 |
| climatology | 0.17 | 0.00 | 0.43 | 0.22 | 0.22 |
| raw point ≥10 (0/1) | 0.24 | -0.40 | 0.58 | 0.13 | 0.22 |
| neighbourhood fraction 45 km | 0.17 | 0.03 | 0.71 | 0.14 | 0.22 |

Best model: **logistic** (BSS 0.11). Shown in the daily report: **yes** (needs BSS ≥ 0.05).

## Reliability of logistic (cross-validated)

| bin | forecasts | mean_forecast | observed_freq |
|---|---|---|---|
| [0.0, 0.1) | 509 | 0.06 | 0.09 |
| [0.1, 0.2) | 497 | 0.14 | 0.14 |
| [0.2, 0.3) | 264 | 0.25 | 0.27 |
| [0.3, 0.5) | 314 | 0.39 | 0.41 |
| [0.5, 0.7) | 108 | 0.57 | 0.48 |
| [0.7, 1.0) | 9 | 0.73 | 0.44 |

BSS > 0 means better than always forecasting the historical event rate; AUC 0.5 = no skill, 1 = perfect ranking.
