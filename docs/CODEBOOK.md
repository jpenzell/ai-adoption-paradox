# Codebook for the current logistic analysis

Source code: `analysis/sentiment_deep_dive.py` and `analysis/survey_2026.py`. This replaces documentation of the withdrawn clustering/random-forest analysis. Numeric stance/trust positions support ordering, filters and plots; the logistic models use the original categorical labels, not ordinal scores.

## Outcomes and eligibility

| Variable | 2025 | 2026 |
|---|---|---|
| `AIUsageScore` | `AISelect`: daily=4, weekly=3, monthly/infrequently=2, plan soon=1, no plan=0 | `AISelect` must select a recognized tool without selecting “I don’t use AI tools”; maximum of available `AIFreq_1..4`: Daily=4, Weekly=3, Monthly or Infrequent=2. Nonuser-only=0; contradictory/unclassified/no-frequency users=missing. |
| `Daily` | 1 when score=4 | 1 when score=4: daily on at least one of four tool types |
| Primary sample | Score≥2 and nonmissing recognized stance/trust | Same rule; stance/trust routing makes all complete cases current users |
| `CodingAssistantDaily` | Not used | `AIFreq_1` equals Daily; single-tool analyses restrict to respondents with nonmissing `AIFreq_1` |
| `HeavyDaily` | Not used | `AIDaily` equals “4+ hours/day”; analyses restrict to respondents who answered the daily-hours item |

Tool types in 2026: AI coding assistants/coding agents, general-purpose AI chat tools, AI agents/automated workflows, and internal company AI tools. Frequency calculations use available responses in all four frequency columns. Routing consistency should be checked against the actual raw data.

## Stance and trust

2025 `AISent` categories: Very unfavorable, Unfavorable, Unsure, Indifferent, Favorable, Very favorable. The display scores are 0–5 in that order. This is not a validated linear scale, and Unsure need not lie between Unfavorable and Indifferent empirically.

2026 `AISentiment` is harmonized for display: Somewhat favorable→Favorable, Neutral→Indifferent, Not sure→Unsure, Somewhat unfavorable→Unfavorable; endpoints unchanged. These position-based labels do not establish measurement equivalence across years.

2025 `AIAcc` categories: Highly distrust, Somewhat distrust, Neither trust nor distrust, Somewhat trust, Highly trust. Display positions are 0–4. The high-distrust subgroup uses Highly distrust.

2026 `AITrust` is copied into `AIAcc` for the shared model code and remains nominal:

- I do not trust it for most work tasks
- I trust it for low-risk work tasks only
- I trust it when I can easily verify the output
- I trust it for many tasks, but not important work decisions
- I trust it for many tasks, including important work decisions
- Not sure / I do not use AI tools

The 2026 subgroup file named `high_distrust` selects “I do not trust it for most work tasks.” Its historical filename does not make that category equivalent to 2025 Highly distrust. The mixed Not sure/nonuse label is retained as a category among otherwise eligible current users.

## Context features

| Feature | Source and recode |
|---|---|
| `WorkExpNum`, `YearsCodeNum` | `WorkExp`, `YearsCode`; commas removed, first semicolon-separated token parsed as float; Less than 1 year→0.5; More than 50 years→51; unparseable→missing |
| `Age` | Raw categorical answer |
| `Professional` | 2025 `MainBranch` is “I am a developer by profession”; 2026 `CodeMain` is “I create code as a primary part of my job” |
| `EmploymentGroup` | First matching rule, in order: Student; Independent contractor/freelancer; Employed; Retired; Not employed; otherwise Other/unknown |
| `PrimaryRole` | Lowercase `DevType` (2025) or `Role` (2026), first keyword match as listed below |
| `OrgBucket` | Just me/Less than 20→Solo/micro;20–99→Small;100–999→Mid-market;1,000–9,999→Large;10,000/More than→Enterprise; otherwise Unknown |
| `WorkMode` | Remote, In-person, Hybrid;2026 Your choice→Flexible; otherwise Unknown |
| `AIThreat` | Raw categorical answer, 2025 only; absent in 2026 |
| `Country` | Raw categorical answer |

Role keyword order: full-stack→Full-stack; back-end→Back-end; front-end→Front-end; data scientist/machine learning→Data/ML; data engineer→Data engineer; devops/platform→DevOps/platform; manager/executive→Management; architect→Architect; security→Security; mobile→Mobile; embedded→Embedded; qa/test→QA/test; student→Student; otherwise Other. First match wins; multiple-role responses are therefore collapsed. The original package reports about 21% of 2025 and 24% of 2026 role answers fall into Other. This affects context models; stance-only and trust-only models do not use this recode.

## Model preprocessing

Within each training fold: numeric median imputation then standardization; categorical most-frequent imputation then one-hot encoding (`handle_unknown="ignore"`, `min_frequency=50`). Explicit recode categories such as Unknown/Other remain categories rather than missing values. Logistic regression uses `lbfgs`, default L 2 regularization (`C=1`), and `max_iter=3000`.

Six fitted specifications: stance only; trust only; context; context+trust; context+stance; context+trust+stance. The reported majority baseline is an analytic constant-prevalence comparator, not a fitted logistic model.

## Historical exclusions

`AIComplexScore`, `AgentScore`, `LearnedAI`, clustering, decision trees, random forests and Gini importance are not part of the current analysis. Historical claims from those models are withdrawn; see `CLAIM_LEDGER.md`.
