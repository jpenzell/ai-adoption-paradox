# Denominators and sample construction

The 2026 counts below were independently recomputed from the official raw CSV. The 2025 figures were checked against the supplied output tables; the 2025 raw data were not freshly rerun. See [release audit](RELEASE_AUDIT.md) and [raw verification](../verification/RAW_DATA_VERIFICATION.md). Different questions and eligibility rules produce different denominators; none should be substituted for another.

## 2026 source and eligibility

The official CSV has 30,903 rows, 122,407,316 bytes, and SHA-256 `ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c`. No duplicate response IDs were found.

| Stage | Respondents | Interpretation |
|---|---:|---|
| Public CSV | 30,903 | All supplied rows |
| Answered AISelect | 17,464 | Includes contradictory answers |
| Selected a tool type without selecting non-use | 14,461 | Noncontradictory self-identified current users |
| Selected non-use only | 2,907 | Non-users |
| Selected both a tool type and non-use | 96 | Excluded as contradictory |
| Current users without recognized tool frequency | 78 | Excluded from frequency analyses |
| Current users with usable frequency | 14,383 | Frequency-eligible users |
| Classifiable use/frequency answers | 17,290 | 14,383 eligible users plus 2,907 non-users |
| Eligible current users with attitude answers | 14,298 | Annual attitude distribution |
| Eligible current users with trust answers | 14,179 | Annual trust distribution |
| Current users with complete use, attitude and trust answers | 14,158 | Primary model and attitude-rate sample |
| Daily users in primary sample | 10,789 | 76.2043% of 14,158 |
| Professional users in primary sample | 11,337 | 80.1%; code is a primary part of their job |

The retained source file `outputs/sentiment_2026/sample_profile.csv` labels 17,290 “Answered AI-use item.” That label actually means classifiable use/frequency answers. The 2026 `answered_ai_use_item` field in `four_year_context.csv` has the same limitation. These original source tables remain unchanged; future profile generation uses the corrected label.

All self-identified current users answering trust, including 30 without usable frequency, would number 14,209. This is not the study's 14,179 trust-distribution denominator. The smaller 14,158 primary sample additionally requires attitude. Neither count describes every survey respondent or all developers.

## 2025 source-table counts

| Stage | Respondents |
|---|---:|
| Public CSV | 49,191 |
| Answered AISelect | 33,720 |
| Complete use, attitude and trust | 33,231 |
| Current users with complete core answers | 26,102 |
| Daily users in primary current-user sample | 15,648 (59.9494%) |
| Professional current users in primary sample | 20,760 |

These values come from `outputs/sentiment/sample_profile.csv` and `current_user_daily_use_by_stance.csv`. The public results website and downloadable CSV can use different counts; this revision does not establish the reason for historical differences and does not attribute them to undocumented filtering.

## 2026 outcome-specific samples

| Outcome | Denominator | n | Outcome share |
|---|---|---:|---:|
| Daily on any tool type | Current users with complete core answers | 14,158 | 76.2% |
| Daily on coding assistants | Primary-sample users answering that tool's frequency item | 11,246 | 73.6% |
| Daily on general chat tools | Primary-sample users answering that tool's frequency item | 10,622 | 66.3% |
| Four-plus hours per day | Primary-sample daily users answering AIDaily | 10,727 | 31.2% |

The tool-specific subsets differ from each other and from the primary sample. Organization-policy and verification-behavior tables also use respondents who answered their respective items. Their cell counts and denominators are retained in the output tables.

## Cross-year context

The historical attitude and trust context tables describe separate voluntary samples. The 2023–2025 trust comparison must restrict denominators consistently to current users; mixing planners or non-users with current users changes the percentages. The 2026 trust item measures nominal conditions for reliance and cannot extend the earlier accuracy-trust scale. Use, attitude and trust wording all changed in 2026. Exact denominator arithmetic does not establish population representativeness or a clean behavioral trend.
