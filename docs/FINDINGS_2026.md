# Findings from the supplied 2026 analysis

The central observation is within 2026: daily use and unfavorable attitudes coexist among current AI users. Of 958 very unfavorable users,520 report daily use on at least one of four tool types (54.3%;95% Wilson interval 51.1–57.4%). Of 4,512 very favorable users,4,195 report daily use (93.0%;92.2–93.7%). Usage therefore does not identify attitude, even though attitude remains associated with frequency.

The 2025 endpoints were 18.8% and 88.1%. These are different cross-sections on different instruments, not a same-question longitudinal change. The endpoint gaps are 69.3 and 38.7 percentage points, respectively; no causal or clean behavioral-change inference follows.

## Within-year discrimination

| Model | 2025 fivefold AUC| 2026 fivefold AUC|
|---|---:|---:|
| Stance only |0.758|0.722|
| Trust only |0.669|0.657|
| Context+trust |0.704|0.713|
| Context+stance |0.790|0.761|
| Context+trust+stance |0.793|0.774|

Context+stance exceeds context+trust in all 50 matched repeated-validation folds in each year. Adding trust to context+stance improves all 50 folds, with mean AUC increments about 0.003 and 0.012. The repeated validation consists of ten repetitions of fivefold CV; folds are not independent studies. The standalone stance-versus-trust ordering also holds in supplied professional-only and country-grouped results. ROC AUC is ranking discrimination, not percent correct or explained variance.

The 2026 trust item concerns scope of reliance, whereas 2025 asks about accuracy. The larger incremental AUC does not establish that trust became more important or that a question redesign caused the increase. The analysis does not establish why the between-model AUC difference changed.

## Denominators and descriptive context

Primary current-user daily prevalence is 59.9% (15,648/26,102) in 2025 and 76.2% (10,789/14,158) in 2026. Coding-assistant daily use is 73.6% among 11,246 respondents answering that frequency item; very unfavorable coding-assistant users report 58.5% (386/660). Chat-tool daily use is 66.3% among 10,622 respondents answering that item. These tool-specific subsets differ from the primary denominator.

The current-user context table reports favorable shares 84.8%,76.8%,72.6%,62.3% for 2023–2026 and unfavorable shares 2.3%,5.7%,9.6%,21.2%. The populations answering these questions, item wording and survey collection changed; use these as reported cross-sectional context, not measurement-invariant attitude estimates. Four annual observations contain three successive decreases.

## 2026-only exploratory/descriptive results

Where respondents say AI use is optional,69.7% report daily use; where AI use is evaluated in performance reviews,88.1% do. Among very unfavorable users, the respective figures are 45.8% (n 203) and 67.6% (n 142). Policy and use are associated; the table does not establish causality, compulsion, resentment, productivity or learning.

Among 10,727 respondents answering daily hours,31.2% report four-plus hours. The relation with stance is nonmonotone:46.0% among very favorable daily users,16.2% among unfavorable and 31.2% among very unfavorable. Stance-only AUC 0.653 indicates some discrimination; “stance does not sort heavy from light use” overstates the result.

Among respondents answering the verification-behavior question, very favorable users more often report using output as-is (15.1% versus 7.1% for very unfavorable) and running it locally (80.0% versus 66.0%), and less often reading official docs (27.9% versus 46.1%). These multiselect responses describe overlapping habits; they do not divide respondents into people who run versus people who read. They are exploratory and do not measure actual verification quality.

## Practical interpretation

A reasonable implication is to ask about attitude and reliance directly alongside use, outcomes and verification habits. This is a proposed measurement practice, not an intervention proven by the survey. The data cannot tell whether more favorable attitudes cause more use, whether workplace policies improve work, or whether heavy use is beneficial.

See `METHODS.md`, `CODEBOOK.md`, `CLAIM_LEDGER.md` and `RELEASE_AUDIT.md`. The latter records which checks were actually run in this revision. Independent 2026 raw-source verification and model reproduction are complete within the documented scope; see `../verification/RAW_DATA_VERIFICATION.md` and `../verification/MODEL_REPRODUCTION.md`. The small country-grouped sensitivity discrepancy is disclosed there. External publication still requires the live-state reconciliation described in the release audit.
