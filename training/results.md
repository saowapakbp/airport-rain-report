# WRFDA 12 UTC correction — cross-validated against SYNOP

2064 airport-days, 71 days (2026-08-02 to 2026-10-11), 34 airports with SYNOP within 15 km; rain ≥10 mm observed 427 times. 5-fold CV grouped by ISO week (test weeks never seen in training). Updated 2026-10-12 18:17 ICT.

| method | MAE | RMSE | bias | cat_match | CSI≥0.1 | CSI≥10 | hit/miss/fa≥10 |
|---|---|---|---|---|---|---|---|
| raw | 8.05 | 19.50 | -2.57 | 0.46 | 0.58 | 0.19 | 113/314/166 |
| bias_region | 9.68 | 21.74 | 0.03 | 0.43 | 0.58 | 0.22 | 147/280/253 |
| quantile_map | 9.64 | 23.10 | -0.15 | 0.44 | 0.55 | 0.21 | 146/281/274 |
| random_forest | 6.91 | 18.56 | -4.44 | 0.38 | 0.58 | 0.08 | 36/391/29 |
| xgboost | 7.04 | 18.59 | -4.25 | 0.38 | 0.58 | 0.09 | 40/387/40 |

raw = nearest grid point; bias_region = per-region multiplicative factor; quantile_map = empirical CDF mapping; random_forest / xgboost = predict log(1+obs) from point and neighbourhood (9/21/45 km) features, region, location, season.

Small sample: treat differences of a few hundredths as noise. Re-run as more days accumulate.
