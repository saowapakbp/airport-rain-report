# P(24 h rain ≥ 10 mm) — WRFDA 12 UTC, cross-validated against AWOS (SYNOP where no AWOS)

2064 airport-days, 71 days (2026-08-02 to 2026-10-11), 427 events (21%). 5-fold CV grouped by ISO week. Updated 2026-10-12 18:17 ICT.

| method | Brier | BSS vs climatology | AUC | mean prob | observed rate |
|---|---|---|---|---|---|
| logistic | 0.15 | 0.11 | 0.73 | 0.20 | 0.21 |
| random_forest | 0.15 | 0.10 | 0.72 | 0.21 | 0.21 |
| xgboost | 0.15 | 0.07 | 0.71 | 0.21 | 0.21 |
| climatology | 0.17 | 0.00 | 0.41 | 0.21 | 0.21 |
| raw point ≥10 (0/1) | 0.23 | -0.40 | 0.58 | 0.14 | 0.21 |
| neighbourhood fraction 45 km | 0.16 | 0.02 | 0.71 | 0.15 | 0.21 |

Best model: **logistic** (BSS 0.11). Shown in the daily report: **yes** (needs BSS ≥ 0.05).

## Reliability of logistic (cross-validated)

| bin | forecasts | mean_forecast | observed_freq |
|---|---|---|---|
| [0.0, 0.1) | 653 | 0.07 | 0.08 |
| [0.1, 0.2) | 568 | 0.14 | 0.15 |
| [0.2, 0.3) | 327 | 0.25 | 0.27 |
| [0.3, 0.5) | 432 | 0.39 | 0.39 |
| [0.5, 0.7) | 79 | 0.56 | 0.43 |
| [0.7, 1.0) | 5 | 0.73 | 0.40 |

BSS > 0 means better than always forecasting the historical event rate; AUC 0.5 = no skill, 1 = perfect ranking.
