# Denominator Reconciliation

This file documents every key count used in the paper alongside the corresponding Stack Overflow published figure and the downloaded CSV count. All three CSV files were downloaded from https://survey.stackoverflow.co/datasets.

---

## CSV File Identifiers

| Year | SHA-256 (first 16 chars) | File Size | Rows |
|---|---|---|---|
| 2025 | `2d1f65308877282e` | 140,893,245 bytes | 49,191 |
| 2024 | `7f2c2dbf6989d00b` | 159,525,875 bytes | 65,437 |
| 2023 | `828874a3cf0fa1bb` | 158,626,799 bytes | 89,184 |

---

## Denominator Table

| Denominator | SO Published | CSV Count | Used in Analysis | Notes |
|---|---|---|---|---|
| **2025 total responses** | 49,009 (methodology page) / 49,019 (results page) | 49,191 | 49,191 | Difference of 172–182 rows. Likely post-publication quality filtering applied to the results page but not yet reflected in the CSV release. The 203,812 combined headline uses CSV counts; SO published figures would yield ~203,630. |
| **2025 AISelect respondents** | 33,662 (AI page) | 33,720 | 33,720 | Difference of 58. Consistent with versioning explanation above. Analytical sample of 33,231 is derived from the CSV figure. |
| **2025 professional developers (total)** | 37,356 (results page) | 37,467 | 37,467 (noted) | Difference of 111. Same versioning gap. |
| **2025 professional developers who answered AISelect** | 26,004 (AI page) | 26,045 | 26,045 | Used to compute 50.6% daily rate, consistent with SO's published 51%. |
| **2025 AIAgents respondents** | 31,877 (AI page) | 31,919 | Not used directly | AgentScore imputed for 1,312 respondents in clustering sample. |
| **2024 total responses** | 65,437 | 65,437 | 65,437 | ✓ Match |
| **2023 total responses** | 89,184 | 89,184 | 89,184 | ✓ Match |
| **2025 countries** | 177 (methodology page) | 177 distinct | 177 | ✓ Match |
| **2024 countries** | 185 (methodology page) | 185 distinct | 185 | ✓ Match |
| **2023 countries** | 185 (methodology page) | 185 distinct | 185 | ✓ Match |

---

## Trust Trend Denominator Shift (Critical)

The trust question routing changed between survey years, creating a comparability issue in the core trust trend.

| Year | Trust Column | Routed To | n | High Trust | High Distrust |
|---|---|---|---|---|---|
| 2023 | AIBen | Current AI users only | 61,396 | 42.2% | 27.2% |
| 2024 | AIAcc | Current AI users only | 37,302 | 43.0% | 30.4% |
| 2025 (paper figures) | AIAcc | All AISelect respondents | 33,297 | 32.8% | 45.7% |
| **2025 (harmonized)** | AIAcc | **Current users only** | **26,126** | **39.3%** | **37.3%** |
| 2025 (non-users only) | AIAcc | Non-users only | 7,171 | 8.9% | 76.5% |

**Conclusion:** The trust decline from 2024 to 2025 is directionally robust on both denominators, but the magnitude differs substantially. The harmonized user-only figures show a smaller — though still meaningful — decline. Non-users show dramatically lower trust, which depresses the 2025 full-denominator figures relative to prior years.

Both the full-denominator and user-only 2025 figures are reported in the paper (Table 2).

---

## AISelect Response Rate Drop (2025)

| Year | Total Respondents | AISelect Answered | Rate |
|---|---|---|---|
| 2023 | 89,184 | 87,973 | 98.6% |
| 2024 | 65,437 | 60,907 | 93.1% |
| 2025 | 49,191 | 33,720 | 68.5% |

The 2025 drop likely reflects a survey redesign routing non-developers away from the AI module. This is an inference from the data pattern; it is not explicitly documented on the 2025 Stack Overflow methodology page.
