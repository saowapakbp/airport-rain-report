# WRFDA 12 UTC correction — cross-validated against SYNOP

1928 airport-days, 67 days (2026-08-02 to 2026-10-07), 34 airports with SYNOP within 15 km; rain ≥10 mm observed 407 times. 5-fold CV grouped by ISO week (test weeks never seen in training). Updated 2026-10-08 22:26 ICT.

| method | MAE | RMSE | bias | cat_match | CSI≥0.1 | CSI≥10 | hit/miss/fa≥10 |
|---|---|---|---|---|---|---|---|
| raw | 8.01 | 18.75 | -2.59 | 0.45 | 0.58 | 0.19 | 104/303/154 |
| bias_region | 9.79 | 21.55 | 0.23 | 0.42 | 0.58 | 0.22 | 139/268/234 |
| quantile_map | 9.73 | 23.25 | 0.03 | 0.43 | 0.55 | 0.21 | 143/264/262 |
| random_forest | 6.89 | 17.69 | -4.26 | 0.39 | 0.60 | 0.10 | 42/365/25 |
| xgboost | 7.05 | 17.73 | -3.90 | 0.39 | 0.60 | 0.11 | 50/357/49 |

raw = nearest grid point; bias_region = per-region multiplicative factor; quantile_map = empirical CDF mapping; random_forest / xgboost = predict log(1+obs) from point and neighbourhood (9/21/45 km) features, region, location, season.

Small sample: treat differences of a few hundredths as noise. Re-run as more days accumulate.
