# 2026 intake decisions

How the 2026 Stack Overflow Developer Survey public CSV was mapped onto the
2025 data contract (repository version 3.1.0), what was decided before the 2026 analysis was run, and
what cannot be compared across years. Code: `analysis/survey_2026.py`.

Data file: `packages/archive/2026/survey_results_public.csv` in
github.com/StackExchange/Survey (Git LFS), SHA-256
`ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c`,
122,407,316 bytes, 30,903 rows. Fielded 2026-06-23 to 2026-08-05; 169
countries. Stack Overflow applied new validity rules in 2026 (consent plus
employment plus not bot-flagged, or all ten core questions answered).

## Comparability decision

All three core items of the 2025 analysis were redesigned in 2026. This
study treats 2026 as a **conceptual replication** of the 2025 design with a
**disclosed wording break**, not as a same-instrument trend. The three
options considered in October 2026 were: (a) conceptual replication with
pre-specified criteria, (b) trend-only with a wording break, (c) hold at
the 2025-only analysis. The study does (a) and reports (b) as context.
Nothing in the 2025 analysis is withdrawn; 2025 remains the same-instrument
anchor.

## Item mapping

| 2025 construct | 2025 item | 2026 item | Mapping | Comparability |
|---|---|---|---|---|
| Current AI use | `AISelect`: "Do you currently use AI tools in your development process?" (single select, frequency built in) | `AISelect`: "Do you currently use AI tools or AI agents in your role at work?" (multi-select across four tool types, plus "I don't use AI tools") | Current user = selected at least one tool type and not "I don't use AI tools". | Scope widened from "development process" to "role at work". |
| Use frequency | Built into `AISelect` (daily / weekly / monthly or infrequently) | `AIFreq_1..4`: frequency per selected tool type (Daily / Weekly / Monthly or Infrequent) | `AIUsageScore` = maximum frequency across the respondent's tool types (4 daily, 3 weekly, 2 monthly). **Daily = daily on any tool type.** | A maximum across up to four items is not the same as one item. Sensitivity: daily on coding assistants alone (`AIFreq_1`). |
| Favorable stance | `AISent`: "How favorable is your stance on using AI tools as part of your development workflow?" Very favorable / Favorable / Indifferent / Unsure / Unfavorable / Very unfavorable | `AISentiment`: "How would you describe your attitude toward using AI tools or agents as part of your work?" Very favorable / Somewhat favorable / Neutral / Not sure / Somewhat unfavorable / Very unfavorable | Position-based: Somewhat favorable to Favorable, Neutral to Indifferent, Not sure to Unsure, Somewhat unfavorable to Unfavorable. Modeled categorically as in 2025. | Same six-point shape; "somewhat" qualifiers and "attitude" wording may shift the distribution. Routed to current users only in 2026. |
| Trust | `AIAcc`: "How much do you trust the accuracy of the output from AI tools as part of your development workflow?" five-point Likert | `AITrust`: "How much do you trust the output from AI tools or AI agents as part of your workflow?" six nominal reliance-scope options (trust when I can verify / many tasks, not important decisions / low-risk tasks only / not for most tasks / including important decisions / not sure) | Kept as its own nominal variable, one-hot encoded as in 2025. The display order in figures is low-to-high reliance and is not a scale. | **Not comparable.** The 2023-2025 Likert trust trend stops at 2025. "Trust vs stance" in 2026 means reliance-scope trust vs stance. |
| Professional | `MainBranch` = "I am a developer by profession" | `CodeMain` = "I create code as a primary part of my job" | Direct substitute. | Close but not identical wording. |
| Role | `DevType` | `Role` | Same `primary_role()` keyword recode. | Response list changed; recode is keyword-based and collapses 24% of 2026 answers to "Other" (21% in 2025), including "AI/ML engineer", "Developer, desktop or enterprise applications", "Academic researcher" and "Cloud infrastructure engineer". Kept unchanged so the context set is the same specification in both years; this is a limitation of the context controls, not of the stance-versus-trust comparison, which does not use it. |
| Work setting | `RemoteWork` (Remote / In-person / Hybrid) | `WorkSetting` (Remote / In-person / two Hybrid variants / "Your choice") | Hybrid variants collapsed to Hybrid; "Your choice" kept as a fourth category, Flexible. | New category. |
| Threat | `AIThreat` | not asked | Dropped from the context set for 2026. | Context set has one fewer variable in 2026. |
| Age, Employment, OrgSize, WorkExp, YearsCode, Country | same names | same names | unchanged recodes | Country missing for 30.8% of 2026 rows (28.0% in 2025); handled by in-fold most-frequent imputation as before. |

## Routing and sample construction (pre-specified)

1. Rows: 30,903.
2. Answered the AI-use item: 17,464. Of these, 2,907 selected only "I don't
   use AI tools" (non-users), 14,461 selected at least one tool type, and 96
   selected both a tool type and "I don't use AI tools". **The 96 contradictory
   rows are excluded** from all samples (they cannot be classified as users or
   non-users). Including them as users (n = 14,252) moves the overall daily rate from
   76.2% to 75.8% and no stance-category rate by more than 1.3 points.
3. Users with no frequency answer on any selected tool type: 78. Excluded
   (no outcome).
4. Stance and trust were routed only to current users in 2026 (0 non-users
   answered either). The complete-case sample on use, stance, and trust is
   therefore entirely current users: **n = 14,158**, of whom 11,337 (80.1%)
   create code as a primary part of their job.
5. Consequence: the 2025 sensitivity contrasts that involved non-users (daily
   vs all other answers, any use vs non-use, use-or-plan vs no plan) cannot be
   formed in 2026. They are replaced by within-user contrasts (weekly-or-more
   vs monthly; coding-assistant daily vs less; four-plus hours vs other daily).

## Pre-specified replication criteria

Set before the 2026 run, mirroring the 2025 claims:

| Criterion | Threshold | 2026 result |
|---|---|---|
| Monotone-ish gradient: very favorable daily rate exceeds very unfavorable by at least 20 points | met if difference >= 20 | 38.7 points (93.0% vs 54.3%): met |
| Stance-only CV AUC exceeds trust-only CV AUC | met if difference > 0.02 | 0.722 vs 0.657: met |
| Context + stance exceeds context + trust in every one of 50 matched splits | met if 50/50 | 50/50: met |
| Adding trust to context + stance still helps | met if 50/50 positive and mean delta > 0 | 50/50, +0.012 AUC: met |
| Country-grouped folds preserve the stance-over-trust ordering | met if ordering holds | 0.721 vs 0.656: met |
| Professional-only subsample preserves the ordering | met if ordering holds | 0.740 vs 0.672: met |

All six criteria were met. The approved language is "replicated on a
redesigned instrument", not "the same result".

## What is new in 2026 and reported as 2026-only

- `AIDaily`: hours per workday among daily users. Used for a four-plus-hours
  contrast among daily users.
- `AIUse`: organizational AI policy. Reported descriptively (daily use by
  stance and policy). Not added to the modeled context set, so the 2026
  models keep the same specification family as 2025.
- Per-tool-type frequency (`AIFreq_1..4`).

## Not done, deliberately

- No reweighting or harmonization model across instruments.
- No pooling of 2025 and 2026 rows into one model.
- No ordinal scoring of the 2026 trust item.
- No causal language anywhere.
