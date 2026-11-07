# 2026 model and exploratory reproduction

Completed 2026-11-07T08:56:29.266090+00:00 by Codex subagent `/root/finish_models`, continuing `/root/audit_analysis` after an app restart.

## Result

The 2026 core statistical pipeline and the exploratory script both finished with exit status 0. **All primary headline results reproduced.** Of 32 expected CSV/JSON artifacts, 30 matched within absolute tolerance 1e-9 and relative tolerance 1e-7; one country-grouped sensitivity table had small differences; one historical four-year context table was intentionally not regenerated. No expected 2026 output was missing. The maximum absolute difference in matching files was 1.02e-13 (floating-point numerical scale).

The matched files include all five-fold primary/context model comparisons, all 50 repeated-fold scores and comparisons, held-out metrics/calibration, raw-column permutation importance, adjusted probabilities, professional-only and alternate-outcome checks, stance/trust and organization-policy tables, and all seven exploratory tables. Descriptive tables matched exactly. Original source tables remain unchanged in the publication package.

## Selected reproduced results

- Primary current users: 14,158; daily users: 10,789 (76.2043%).
- Five-fold AUC: attitude only 0.722; trust only 0.657; context plus attitude 0.761; context plus trust 0.713.
- Context plus attitude exceeded context plus trust in all 50 matched repeated-validation folds. Adding trust to context plus attitude also improved AUC in all 50 folds.
- Held-out AUC: 0.7720128402218782; calibration slope: 0.9103245451319483.

## Country-grouped sensitivity discrepancy

| Model | Supplied mean AUC | Rerun mean AUC |
|---|---:|---:|
| Attitude only | 0.7205880825 | 0.7206860730 |
| Trust only | 0.6557626922 | 0.6558800555 |
| Context plus trust plus attitude | 0.7691685753 | 0.7691664483 |

Nine cells in `primary_country_grouped_cv.csv` differ beyond the strict tolerance. The largest absolute difference, 0.0009246622, is in the standard deviation of attitude-only AUC. The stance-versus-trust ordering is unchanged. This is a disclosed numerical reproduction difference, not an exact match.

The installed scikit-learn GroupKFold balances country sizes using NumPy's default unstable argsort, and 112 countries share their sample size with at least one other country. A probe changing only the ordering of tied group sizes altered the sensitivity metrics at a similar scale while preserving the ordering. The original country-to-fold assignments and full original environment were not supplied, so this does **not** establish the exact cause of the discrepancy. `country-fold-probe.json` records country-to-fold mappings for the current default, stable-sort, and heapsort probes. The exact rerun table is in `country_grouped_cv_rerun.csv`.

## Inputs and scope

The raw CSV came from the official StackExchange/Survey archive and matched SHA-256 `ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c`. Independent raw-source checks are documented in `RAW_DATA_VERIFICATION.md`; those checks did not import the project analysis code. This model reproduction runs the project's code with an isolated environment.

Only three execution changes were made to the supplied core script: cap parallel jobs at two (and BLAS threads at one), require the 2026 input only, and skip the historical four-year context rebuild. The scope patch is included. All 2026 core computations remained unchanged. Original 2025 output tables were read solely to construct the two-year comparison table; the 2025 models and 2023–2025 raw data were not freshly rerun here. The 2026 denominators in the retained context table were independently checked against raw data separately.

Pandas 2.3.3 and scikit-learn 1.6.1 match the package's pins. The complete resolved environment is `model-environment-freeze.txt`. SciPy 1.18.1 emitted `OptimizeWarning: Unknown solver options: iprint` from scikit-learn's optimizer wrapper; this is recorded in the log. No convergence warning or failed fit was reported, and the main metrics matched to floating-point precision. Exact versions and the current fold assignments are preserved to support future reproduction.

## Commands used

From the isolated `work/rerun2026` directory, with its installed virtual environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ../rerun2026-venv/bin/python -u analysis/sentiment_deep_dive.py --year 2026
../rerun2026-venv/bin/python -u analysis/exploratory_2026.py
../rerun2026-venv/bin/python compare_outputs.py
```

For a later output comparison, the packaged comparison script accepts explicit `--expected`, `--actual`, and optional `--output` paths. The raw CSV and virtual environment are not bundled in the publication package. The retained primary figures and revised presentation assets use the supported headline results; the figure-title changes do not alter the statistical outputs.
