# P(24 h rain ≥ 10 mm) — WRFDA 12 UTC, cross-validated against SYNOP

1895 airport-days, 64 days (2026-08-02 to 2026-10-04), 386 events (20%). 5-fold CV grouped by ISO week. Updated 2026-10-05 17:48 ICT.

| method | Brier | BSS vs climatology | AUC | mean prob | observed rate |
|---|---|---|---|---|---|
| logistic | 0.15 | 0.09 | 0.71 | 0.22 | 0.20 |
| random_forest | 0.15 | 0.11 | 0.72 | 0.22 | 0.20 |
| xgboost | 0.15 | 0.09 | 0.72 | 0.21 | 0.20 |
| climatology | 0.16 | 0.00 | 0.40 | 0.20 | 0.20 |
| raw point ≥10 (0/1) | 0.23 | -0.39 | 0.58 | 0.13 | 0.20 |
| neighbourhood fraction 45 km | 0.16 | 0.04 | 0.71 | 0.14 | 0.20 |

Best model: **random_forest** (BSS 0.11). Shown in the daily report: **yes** (needs BSS ≥ 0.05).

## Reliability of random_forest (cross-validated)

| bin | forecasts | mean_forecast | observed_freq |
|---|---|---|---|
| [0.0, 0.1) | 479 | 0.06 | 0.08 |
| [0.1, 0.2) | 534 | 0.15 | 0.12 |
| [0.2, 0.3) | 373 | 0.25 | 0.24 |
| [0.3, 0.5) | 378 | 0.38 | 0.33 |
| [0.5, 0.7) | 110 | 0.58 | 0.55 |
| [0.7, 1.0) | 21 | 0.73 | 0.52 |

BSS > 0 means better than always forecasting the historical event rate; AUC 0.5 = no skill, 1 = perfect ranking.
