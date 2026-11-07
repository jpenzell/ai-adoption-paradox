# Independent raw-data verification

Completed 2026-11-07T03:44:44.195816+00:00 by Codex subagent /root/raw_verification.

Source: https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2026/survey_results_public.csv

Full file: `data/2026/survey_results_public.csv` (download separately; raw CSV is not bundled) (122,407,316 bytes). SHA-256: `ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c`. The full downloaded file exactly matches the supplied expected checksum. It was assembled from HTTP206 byte-range downloads; the final full-file hash, not individual chunk presence, established completeness.

Recomputation: `python3 verification/verify_2026.py --csv data/2026/survey_results_public.csv` from the research directory. Python standard library only; no project analysis code or helpers imported. Detailed output: `verification/raw-verification-results.json`.

## Verified results

- Raw rows: 30,903; duplicate ResponseId values: zero.
- Answered AISelect: 17,464. This consists of 14,461 noncontradictory self-identified current users, 2,907 non-users, and 96 contradictory tool-plus-non-use selections.
- Of 14,461 self-identified users, 78 supplied no recognized frequency answer. The study's frequency-eligible current-user denominator is therefore 14,383. The study's use-item denominator 17,290 excludes the 96 contradictions and 78 missing-frequency user records.
- Primary complete-case current users: 14,158. Daily: 10,789 (76.2043%).
- Very unfavorable: 520/958 daily (54.2797%). Very favorable: 4,195/4,512 (92.9743%).
- Every one of the six primary stance rows agrees with the supplied counts and rates. Every one of the 49 organization-policy cells agrees with supplied denominators and rates (absolute rate tolerance 1e-12).
- Very unfavorable/optional policy: 93/203 daily (45.8128%); very unfavorable/measured in performance: 96/142 (67.6056%).
- Current-user trust distribution denominator: 14,179, requiring valid use frequency; all six category shares match the supplied table. The 2026 source-table current-user, use-item, attitude, and trust denominators all pass.
- All self-identified current users with trust answers, including missing-frequency records, would instead give 14,209. Do not describe 14,179 as including every self-identified current user.
- Current-user attitude distribution denominator: 14,298, also requiring valid use frequency.
- Daily classification using any reported frequency versus only the frequencies of selected tool types differs for zero eligible users.

## Scope

The check establishes 2026 raw-data provenance and the headline descriptive calculations. This independent script checks descriptive calculations. Model AUC, cross-validation, calibration and permutation importance were reproduced separately; see [model reproduction](MODEL_REPRODUCTION.md). The 2025 data were not independently recomputed in this script. The survey remains a voluntary repeated cross-section, with redesigned items in 2026; exact arithmetic does not resolve causal or cross-year comparability limits.
