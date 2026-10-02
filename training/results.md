# WRFDA 12 UTC correction — cross-validated against SYNOP

1701 airport-days, 61 days (2026-08-02 to 2026-10-01), 28 airports with SYNOP within 15 km; rain ≥10 mm observed 369 times. 5-fold CV grouped by ISO week (test weeks never seen in training). Updated 2026-10-03 00:34 ICT.

| method | MAE | RMSE | bias | cat_match | CSI≥0.1 | CSI≥10 | hit/miss/fa≥10 |
|---|---|---|---|---|---|---|---|
| raw | 8.12 | 19.45 | -3.12 | 0.44 | 0.58 | 0.19 | 93/276/131 |
| bias_region | 10.22 | 22.54 | 0.14 | 0.41 | 0.59 | 0.23 | 132/237/217 |
| quantile_map | 10.52 | 25.80 | 0.37 | 0.42 | 0.56 | 0.22 | 135/234/239 |
| random_forest | 7.17 | 18.83 | -4.57 | 0.40 | 0.61 | 0.11 | 42/327/30 |
| xgboost | 7.30 | 18.91 | -4.37 | 0.40 | 0.61 | 0.12 | 49/320/43 |

raw = nearest grid point; bias_region = per-region multiplicative factor; quantile_map = empirical CDF mapping; random_forest / xgboost = predict log(1+obs) from point and neighbourhood (9/21/45 km) features, region, location, season.

Small sample: treat differences of a few hundredths as noise. Re-run as more days accumulate.
