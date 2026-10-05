# WRFDA 12 UTC correction — cross-validated against SYNOP

1895 airport-days, 64 days (2026-08-02 to 2026-10-04), 28 airports with SYNOP within 15 km; rain ≥10 mm observed 386 times. 5-fold CV grouped by ISO week (test weeks never seen in training). Updated 2026-10-05 17:48 ICT.

| method | MAE | RMSE | bias | cat_match | CSI≥0.1 | CSI≥10 | hit/miss/fa≥10 |
|---|---|---|---|---|---|---|---|
| raw | 7.77 | 18.73 | -2.91 | 0.45 | 0.57 | 0.18 | 96/290/143 |
| bias_region | 9.63 | 21.42 | 0.17 | 0.43 | 0.58 | 0.22 | 137/249/229 |
| quantile_map | 9.68 | 23.55 | 0.06 | 0.44 | 0.55 | 0.21 | 136/250/249 |
| random_forest | 6.86 | 18.03 | -4.24 | 0.39 | 0.59 | 0.11 | 45/341/25 |
| xgboost | 6.98 | 17.97 | -3.88 | 0.39 | 0.59 | 0.13 | 54/332/43 |

raw = nearest grid point; bias_region = per-region multiplicative factor; quantile_map = empirical CDF mapping; random_forest / xgboost = predict log(1+obs) from point and neighbourhood (9/21/45 km) features, region, location, season.

Small sample: treat differences of a few hundredths as noise. Re-run as more days accumulate.
