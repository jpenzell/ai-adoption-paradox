# Release audit — November 2026

This revision was prepared from the user-supplied review package. Fresh public GitHub API and git reads confirmed that its base commit is `365e808137a4746be2548d374a6f75d4af357ddf` on `v3.2.0-2026-update`. At that check, default branch `main` was `67d1b11019d7b1add44a7dba1a1baf74cd55c65e` and still presented the 2025 analysis. No remote push, merge, website publication, or LinkedIn post was performed in this revision. The 2025 publication remains a historical version; this review concerns the 2026 revision.

## Verified results and scope

The official 2026 CSV contains 30,903 rows and no duplicate response IDs. Its 122,407,316 bytes match SHA-256 `ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c`. Independent standard-library calculations, without importing the project analysis code, reproduced all six stance rows, 49 organization-policy cells, six trust shares, and relevant 2026 denominators. The primary sample is 14,158 current users with complete core answers; 10,789 report daily use. The unfavorable and favorable endpoints are 520/958 and 4,195/4,512. See [raw verification](../verification/RAW_DATA_VERIFICATION.md), [results](../verification/raw-verification-results.json), and [portable verifier](../verification/verify_2026.py).

The separate 2026 core and exploratory model reruns finished successfully on 2026-11-07 UTC. Thirty CSV/JSON artifacts matched within absolute tolerance 1e-9 and relative tolerance 1e-7, including all headline model results, all 50 repeated-validation folds, held-out calibration, permutation importance, standardized probabilities, alternate outcomes, professional-only checks, and all seven exploratory tables. The largest difference among matching files was 1.02e-13. No convergence warning or failed fit was reported.

One country-grouped sensitivity table differed slightly: mean AUC differences were at most 0.000118, and the largest difference across all its cells was 0.000925 in an AUC standard deviation. Model ordering was unchanged. Tied country-size ordering is a plausible numerical contributor, but the exact cause is not established. The original and rerun tables, diagnostic fold assignments, logs, execution-scope patch and environment are preserved. See [model reproduction](../verification/MODEL_REPRODUCTION.md) and [comparison](../verification/model-comparison-report.json).

The historical four-year table was intentionally not regenerated. Its 2026 denominators were independently checked against raw data. The 2025 counts, rates and model comparisons were audited against the supplied tables; the 2025 raw data and models were not freshly rerun. The supplied 2025 tables show 15,648/26,102 daily users and 50 positive context-plus-stance versus context-plus-trust differences. Those table checks are distinct from the 2026 raw-data and model reproductions.

## Repairs and preservation

- Replaced the obsolete clustering/random-forest codebook with the actual logistic-model recodes.
- Specified repeated validation as three context models, ten repeats of five folds, seed 719. Main five-fold CV and the held-out split use seed 42. Preprocessing is fitted within training-fold pipelines.
- Removed unsupported causal explanations, population claims, unqualified cross-year trends, and claims that every survey predictor was compared.
- Clarified current-user, complete-case and tool-specific denominators. In particular, trust n=14,179 requires usable frequency and trust answers; including 30 current-tool users without usable frequency would give n=14,209.
- Added a portable downloader with checksum validation, temporary downloads, and explicit handling of mismatched existing files.
- Corrected future sample-profile label generation. The retained 2026 profile's original label “Answered AI-use item” represents 17,290 classifiable use/frequency answers, not 17,464 raw AISelect answers. The four-year table has the same naming limitation.
- Revised two figures to make separate annual samples and the 2026 measurement break explicit; see [figure revisions](../verification/FIGURE_REVISIONS.md).

All 50 original statistical CSV/JSON files remain unchanged. Presentation figures and public copy were revised; model estimates were not replaced with the rerun values. Python syntax checks passed. The downloader passed local-fixture checks for a successful download, a valid cached input, refusal to overwrite a mismatched input, rejection of a bad downloaded hash without altering the old input, and replacement only after successful verification.

## Limits and publication checks

No contemporaneous preregistration, literature novelty, or population representativeness was established. Voluntary cross-sections, complete-case selection, self-report and redesigned 2026 measures constrain interpretation. The overlapping repeated folds are not independent replications.

Before external publication, inspect the current repository head and publish the verified revision or replace generic analysis links with its final destination. Do not advertise the default branch as the revised 2026 release until it contains that release. This audit records local preparation and verification, not completed external publication.
