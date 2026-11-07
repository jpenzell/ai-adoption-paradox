# Isolated 2026 reproduction

Input: verified official 2026 raw CSV symlinked from ../verified-data/2026.csv. Parent/raw-verification task confirms source and SHA separately. Original 2025 output tables copied only to construct the two-year comparison; they are not a fresh 2025 reproduction.

Changes to original script for this run only:
- n_jobs capped at 2 (BLAS threads capped externally at 1).
- Startup existence check only requires 2026; run rejects other years.
- Historical four_year_context CSV/figure rebuild skipped, so 2023–2025 raw files are not prerequisites.

All 2026 core computations are unchanged: descriptive rates, all core and sensitivity logistic models, main CV, 50 matched repeated-CV folds, country groups, held-out calibration, permutation importance, standardized probabilities, policy and tool-specific outcomes. The 2026 exploratory script also completed successfully in a separate run; see MODEL_REPRODUCTION.md.


Raw source confirmation received from `/root/raw_verification`: SHA-256 `ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c`, matching independently recalculated hash in this task. All four tool-frequency columns have zero answered values for unselected tool types, so taking their maximum matches selected-tool-only maximum exactly.

Trust denominator clarification: the four-year context source table uses 14,179 noncontradictory current users with usable frequency AND a trust response. There are 14,209 self-identified current-tool users answering trust if the 30 without usable frequency are included. The primary complete-case sample is 14,158. This run does not rebuild the four-year context table, so that separate denominator check comes from raw verification, not that skipped code path.
