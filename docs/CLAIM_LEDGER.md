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

## Note on presentation assets

Any slide, carousel, or talk asset reporting a random-forest Gini importance share — including a "4.6x" ratio between stance and accuracy trust — reflects the withdrawn analysis and should be rebuilt from the current outputs in `outputs/sentiment/`.

Impurity-based importance is unreliable when predictors are correlated, and stance and accuracy trust are correlated here. The defensible figures are the descriptive gradient (18.8% to 88.1%) and the cross-validated AUC comparison (0.758 stance alone versus 0.669 accuracy trust alone).
