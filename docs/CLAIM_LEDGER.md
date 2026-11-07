# Claim ledger

Every substantive claim in this project, its evidence status, and the language approved for publication. Claims marked *Removed* or *Not supported* appeared in earlier versions of this work and must not be cited.

| Claim | Evidence status | Publication language |
|---|---|---|
| AI use rose while trust weakened from 2023 to 2025. | Descriptive context only; survey wording, routing, and samples differ. | "Reported use rose while harmonized trust weakened across repeated cross-sections." |
| Stance and accuracy trust are distinct survey items. | Supported by item wording and different incremental classification value. This does not prove clean latent-construct separation. | "The two items are analytically distinct and non-interchangeable here." |
| Among current users, daily use is 18.8% at very unfavorable and 88.1% at very favorable. | Supported in the primary n=26,102 sample. | Report endpoints, denominators, and the unsure/indifferent reversal. |
| Stance contains more classification information than trust for current-use frequency. | Supported by common-fold CV, 50 matched splits, professional-only and country-grouped checks. | "Stance carries substantially more information about reported daily use in this sample." |
| Adding trust to context + stance still helps slightly. | Supported; mean five-fold AUC rises from 0.790 to 0.793 and all 50 repeated comparisons are positive. | Keep "slightly"; do not call trust irrelevant. |
| The finding is novel. | The exact current-user, stance-versus-accuracy-trust comparison appears narrower than the broad published adoption/trust narrative, but no systematic-review claim is made. | "A distinct secondary analysis" or "a narrower contribution," not "the first." |
| Stance causes daily use. | Not supported. | Do not claim. |
| Increasing employee sentiment will increase adoption. | Not supported; needs longitudinal or experimental evidence. | At most a testable hypothesis. |
| High trust is desirable. | Not established without reliability and calibration evidence. | Recommend calibrated reliance, not maximum trust. |
| Full-sample endpoint separation proves the main claim. | Overstated because the stance item is close to current-use status. | Use the current-user comparison as primary; label full-sample results sensitivity only. |
| Structured AI learning drives adoption. | Not supported by the available learning-route field. | Removed. |
| Five stable developer archetypes exist. | Not supported by the earlier clustering diagnostics. | Removed. |
| Random-forest Gini share proves stance dominance. | Not supported as a standalone inference. | Replaced with nested CV and held-out permutation checks. |
| Stack Overflow respondents represent all developers. | Not supported. | Name the voluntary sample; avoid population-prevalence claims. |

## 2026 claims (v3.2.0)

| Claim | Evidence status | Publication language |
|---|---|---|
| The stance-over-trust ordering replicated in 2026. | Supported: all six pre-specified criteria met on the redesigned instrument (INTAKE_DECISIONS_2026.md). | "Replicated on a redesigned instrument"; never "the same result" or "unchanged." |
| Among 2026 current users, daily use is 54.3% at very unfavorable and 93.0% at very favorable. | Supported in the primary n=14,158 sample; coding-assistant-only and chat-only outcomes give 58.5%/87.9% and 47.7%/81.5%. | Report endpoints, denominators, and that "daily" is daily on any of four tool types. |
| Daily use among unfavorable users rose sharply from 2025 to 2026. | Supported in direction; the magnitude crosses an instrument change (single item to per-tool maximum; "development process" to "role at work"). | "The floor rose"; give both years' wording; do not report the 35-point gap as a measured change in behavior. |
| Daily use among current users rose from 60% to 76%. | Supported in direction; partly measurement. Coding assistants alone 73.6%. | Always pair with the single-tool figure. |
| Favorable stance among users fell for a fourth year. | Supported in direction with a current-user denominator in every year; 2026 added "somewhat" qualifiers. | "Kept falling"; flag the label change. |
| The redesigned reliance-scope trust item carries more incremental information than the accuracy item did. | Supported (+0.012 vs +0.003 AUC over context + stance; permutation importance 0.038 vs 0.006), but it is a different question on a different sample. | "Carries more information in 2026 than the accuracy item did in 2025"; not "trust matters more now." |
| The 2023-2025 trust decline continued in 2026. | Not testable: the 2026 item is not on the Likert scale. | Do not claim. Stop the trust trend line at 2025. |
| Stance does not separate heavy (4+ h/day) from light daily use. | Supported descriptively (AUC 0.653 vs trust 0.644; non-monotone pattern). | Observation only; name the U-shape and both readings. |
| Organizational measurement of AI use is associated with higher daily use, including among unfavorable users. | Supported descriptively (69.7% optional vs 88.1% measured; 45.8% vs 67.6% among very unfavorable). 2026-only item. | Association; do not say measurement causes use or resentment. |
| Developers use AI daily whether or not they like it. | Supported as a summary of the 2026 cross-section. | Acceptable headline; pair with "self-reported" and "Stack Overflow respondents." |

## Note on presentation assets

Any slide, carousel, or talk asset reporting a random-forest Gini importance share — including a "4.6x" ratio between stance and accuracy trust — reflects the withdrawn analysis and should be rebuilt from the current outputs in `outputs/sentiment/`.

Impurity-based importance is unreliable when predictors are correlated, and stance and accuracy trust are correlated here. The defensible figures are the descriptive gradient (18.8% to 88.1% in 2025; 54.3% to 93.0% in 2026) and the cross-validated AUC comparison (0.758 versus 0.669 in 2025; 0.722 versus 0.657 in 2026). Assets built from v3.1.0 that show only 2025 are not wrong; they are dated.
