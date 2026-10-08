# P(24 h rain ≥ 10 mm) — WRFDA 12 UTC, cross-validated against AWOS (SYNOP where no AWOS)

1928 airport-days, 67 days (2026-08-02 to 2026-10-07), 407 events (21%). 5-fold CV grouped by ISO week. Updated 2026-10-08 22:26 ICT.

| method | Brier | BSS vs climatology | AUC | mean prob | observed rate |
|---|---|---|---|---|---|
| logistic | 0.15 | 0.08 | 0.71 | 0.23 | 0.21 |
| random_forest | 0.15 | 0.10 | 0.72 | 0.23 | 0.21 |
| xgboost | 0.15 | 0.08 | 0.72 | 0.22 | 0.21 |
| climatology | 0.17 | 0.00 | 0.42 | 0.21 | 0.21 |
| raw point ≥10 (0/1) | 0.24 | -0.41 | 0.58 | 0.13 | 0.21 |
| neighbourhood fraction 45 km | 0.16 | 0.02 | 0.70 | 0.15 | 0.21 |

Best model: **random_forest** (BSS 0.10). Shown in the daily report: **yes** (needs BSS ≥ 0.05).

## Reliability of random_forest (cross-validated)

| bin | forecasts | mean_forecast | observed_freq |
|---|---|---|---|
| [0.0, 0.1) | 462 | 0.05 | 0.08 |
| [0.1, 0.2) | 523 | 0.15 | 0.12 |
| [0.2, 0.3) | 394 | 0.25 | 0.23 |
| [0.3, 0.5) | 420 | 0.38 | 0.35 |
| [0.5, 0.7) | 116 | 0.58 | 0.53 |
| [0.7, 1.0) | 13 | 0.74 | 0.38 |

BSS > 0 means better than always forecasting the historical event rate; AUC 0.5 = no skill, 1 = perfect ranking.
