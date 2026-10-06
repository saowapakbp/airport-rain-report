# Stage 1 — distributional (quantile) correction of WRFDA 24 h rain, 12Z + 18Z

1812 airport-days, 65 days (2026-08-02 to 2026-10-05), SYNOP within 15 km; rain ≥10 mm observed 387 times. 5-fold CV grouped by ISO week. Updated 2026-10-06 19:45 ICT.

## Rain amount

| method | MAE | bias | cat_match | CSI≥0.1 | CSI≥10 | ≥10 hit/miss/fa | fc≥35 & obs<10 |
|---|---|---|---|---|---|---|---|
| raw point 12Z | 8.14 | -2.86 | 0.44 | 0.58 | 0.19 | 100/287/142 | 18 |
| report now (12Z area mean) | 7.34 | -2.88 | 0.46 | 0.58 | 0.22 | 116/271/134 | 5 |
| 12Z+18Z area mean | 7.24 | -2.53 | 0.45 | 0.60 | 0.24 | 131/256/151 | 4 |
| quantile model q10 | 7.42 | -7.42 | 0.40 | 0.02 | 0.00 | 0/387/0 | 0 |
| quantile model q50 | 6.84 | -4.53 | 0.42 | 0.60 | 0.18 | 77/310/44 | 0 |
| quantile model q90 | 11.64 | 5.95 | 0.29 | 0.60 | 0.30 | 321/66/681 | 18 |

Quantile loss (lower is better): q10 0.74, q50 3.42, q90 3.44. Observed value inside the q10–q90 range: 82% (ideal 80%).

## P(rain ≥ 10 mm)

| method | Brier | BSS | AUC |
|---|---|---|---|
| current logistic (12Z) | 0.15 | 0.09 | 0.72 |
| new (12Z+18Z, GBM) | 0.16 | 0.02 | 0.71 |
