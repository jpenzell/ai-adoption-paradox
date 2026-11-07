# Methods

## Design and question

A secondary analysis of repeated cross-sectional Stack Overflow Developer Survey public-use CSVs. The supplied package analyzes 2025 and 2026 separately and uses 2023–2025 for descriptive context. The question is whether favorable stance and the survey trust item carry different information about contemporaneously reported daily versus less-frequent AI use among current users. This is neither causal estimation nor forecasting.

All three core questions changed in 2026. Use broadened from development process to role at work and became a four-tool frequency maximum. Stance labels/wording changed. Trust changed from an accuracy scale to nominal reliance-scope options. Consequently, within-year comparisons are primary. Across-year percentages describe different samples/instruments; they do not identify either the size or direction of underlying behavioral change independently of measurement and sample changes.

The original package calls its six 2026 criteria pre-specified. This local revision has not independently established when the criteria were fixed; no claim of public preregistration is made. See `INTAKE_DECISIONS_2026.md` and `RELEASE_AUDIT.md`.

## Samples and denominators

2025 supplied counts:49,191 raw rows;33,720 AI-use answers;33,231 complete cases on use, stance and trust;26,102 current users in the primary sample, including 20,760 professional developers. Daily prevalence is 15,648/26,102=59.95%.

2026 supplied counts:30,903 raw rows;17,464 AI-use answers;96 contradictory tool+nonuse answers excluded;78 otherwise classified users lacking frequency excluded. This leaves 17,290 classifiable use/frequency answers. Stance/trust are routed to current users, producing 14,158 primary complete cases, including 11,337 people creating code as a primary job activity. Daily prevalence is 10,789/14,158=76.20%.

The single-tool sensitivity subsets have different denominators:11,246 primary-sample respondents answering coding-assistant frequency, and 10,622 answering chat-tool frequency. Their daily rates cannot be compared with any-tool percentages as though denominators were identical. Heavy daily-use analysis uses 10,727 respondents answering the daily-hours item. No survey weights are available.

## Descriptive analysis

Report daily-use proportions and 95% Wilson intervals across six stance categories, without forcing a monotone relationship. In both years, Unsure reports more daily use than Indifferent/Neutral. Stance-by-trust matrices report rates and cell sizes. Wilson intervals summarize binomial variation conditional on the observed sample and do not correct voluntary-survey selection.

## Models and validation

Six logistic models use categorical stance/trust and the context variables in `CODEBOOK.md`: stance only, trust only, context, context+trust, context+stance, context+trust+stance. A seventh reported row is a constant-prevalence majority baseline, not a fitted logistic model.

The main comparison uses the same five stratified folds (`shuffle=True`, seed 42). Metrics are accuracy, balanced accuracy, ROC AUC, log loss and Brier score. ROC AUC describes ranking discrimination; it is not classification accuracy or the fraction of behavior explained. Numeric median imputation/scaling and categorical most-frequent imputation/one-hot encoding are fitted inside each training fold.

Repeated validation covers **three context models only**: context+trust, context+stance and context+trust+stance. `RepeatedStratifiedKFold(n_splits=5,n_repeats=10,random_state=719)` yields 50 matched 80/20 train/test folds. These folds overlap and are not 50 independent replications. Report the number of positive paired AUC differences and their empirical 2.5 th/97.5 th percentiles as split variability, not population confidence intervals.

Fivefold `GroupKFold` uses observed country as the grouping variable and excludes missing-country records. Supplied country-grouped outputs contain 173 countries in 2025 and 157 in 2026. Countries do not cross train/test within a fold. Raw country encoding, including infrequent categories, is learned inside training folds. Professional-only subsets use the same model specifications. These checks do not establish representativeness or measurement invariance.

An additional stratified 80/20 split (seed 42) evaluates the complete context+trust+stance model. Report held-out metrics, logistic recalibration intercept/slope and the weighted mean absolute calibration gap across prediction deciles. Raw-column permutation importance uses 20 test-set permutations, seed 42. Interpret correlated-predictor importance alongside nested-model comparisons. It is not a causal effect.

## Sensitivity analyses

2025: daily versus all other answers, weekly-or-more versus the remainder, any use versus nonuse, use-or-plan versus no plan, and professional current users. Broader contrasts are secondary because the stance question is close to use/nonuse status.

2026: daily versus less frequent, weekly-or-more versus monthly, daily coding-assistant use among respondents answering that item, four-plus hours among daily-hours respondents, and professional current users. Nonuser contrasts cannot be formed with complete stance/trust under 2026 routing.

2026 organizational policy and additional workflow/verification/job-satisfaction tables are descriptive. Exploratory analyses were not part of the stated replication criteria. The heavy-use relationship is nonmonotone; this does not mean stance has no classification information.

## Interpretation and computational status

The same-wave voluntary self-reports cannot establish whether stance precedes use, follows experience, reflects usefulness/job fit, or rationalizes behavior. Selection, routing, complete-case exclusions and common-method bias remain. Stance/trust are individual items, not validated multi-item scales. Role keyword recoding is coarse. All conclusions are conditional on the sampled respondents.

Seed 42 controls main CV, held-out split and permutation importance; repeated CV uses 719. `requirements.txt` pins pandas 2.3.3 and scikit-learn 1.6.1; other libraries have version ranges, so numerical comparisons should allow floating-point tolerance. The original package reports independent reproduction; this revision's actual checks are recorded separately in `RELEASE_AUDIT.md`. Existing output files are preserved source artifacts, not represented as newly recomputed here.
