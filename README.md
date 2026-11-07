# Adoption Without Confidence?

**Favorable Stance, Trust, and Reported AI-Use Frequency in the 2025 and 2026 Stack Overflow Surveys**

Josh Penzell · Imagination Applied Open Research Series · **First release, November 2026** (repository version 3.2.0)

> **This is the first public write-up of this work, and it covers two survey years.** The 2025 analysis was completed and independently reproduced before the 2026 data were released; the 2026 survey was then run as a conceptual replication of the 2025 design, with pre-specified criteria and the wording break disclosed, because Stack Overflow redesigned the use, stance, and trust items in 2026. The 2026 results and what changed are in [`docs/FINDINGS_2026.md`](docs/FINDINGS_2026.md); the mapping and pre-specified criteria are in [`docs/INTAKE_DECISIONS_2026.md`](docs/INTAKE_DECISIONS_2026.md).

---

> ### ⚠️ Repository history
>
> Earlier commits in this repository (before internal version 3.1.0, never released) contained an earlier analysis titled *"Human–AI Work Patterns in Software Development: Archetypes, Paradoxes, and the Decline of Trust,"* built on k-means/k-modes clustering, association rule mining, and random-forest Gini importance.
>
> **Several claims from that version have been formally withdrawn.** They are listed under *Withdrawn claims* below and documented in [`docs/CLAIM_LEDGER.md`](docs/CLAIM_LEDGER.md). Please do not cite the earlier manuscripts (`adoption_paper_v34`, `v40`) or the archetype/random-forest findings. The current analysis supersedes them.

---

## What this study asks

Among developers **already using AI tools**, does a favorable *stance* toward AI carry different information about reported daily-use frequency than *trust in the accuracy* of AI output?

Stack Overflow has already reported the broad headline that AI use rose while trust weakened. This is a narrower question about construct separation — not a causal study, and not a forward-prediction model.

## Headline results

Primary sample: **26,102** current AI users from the 2025 public CSV (49,191 rows → 33,720 answered the AI-use item → 33,231 complete cases on use, stance, and trust). Daily-use prevalence 59.9%.

- Daily use rises from **18.8%** among very unfavorable current users to **88.1%** among very favorable.
- The six stance categories are modeled **categorically and are not monotonic**: unsure respondents report more daily use (34.0%) than indifferent respondents (31.5%). This is disclosed, not smoothed.
- Five-fold cross-validated **ROC AUC: 0.758 for stance alone, 0.669 for accuracy trust alone.**
- Adding stance to context + trust raises AUC from **0.704 → 0.793**. Adding trust to context + stance raises it from **0.790 → 0.793** — trust still contributes; it is not irrelevant.
- The stance advantage holds in all 50 matched repeated splits, in professional-only and country-grouped checks, with held-out AUC 0.789 and calibration slope 0.96.

## 2026 replication (headline)

Primary sample: **14,158** current AI users from the 2026 public CSV (30,903 rows; stance and trust were routed to current users only). Daily-use prevalence 76.2%, where daily means daily on at least one of four tool types (coding assistants alone: 73.6%).

- Daily use rises from **54.3%** among very unfavorable current users to **93.0%** among very favorable. In 2025 the same endpoints were 18.8% and 88.1%: the floor rose, the ceiling barely moved, and the gradient compressed from 69 to 39 points.
- Five-fold cross-validated **ROC AUC: 0.722 for stance alone, 0.657 for the redesigned reliance-scope trust item alone.** Context + stance 0.761 vs context + trust 0.713; all three 0.774. Stance beat trust in all 50 matched splits, as in 2025, but the margin narrowed (0.087 to 0.048).
- The reliance-scope trust item adds more over context + stance than the 2025 accuracy item did (+0.012 vs +0.003 AUC).
- Favorable stance among current users: 84.8% (2023), 76.8%, 72.6%, **62.3%** (2026). Unfavorable: 2.3%, 5.7%, 9.6%, **21.2%**.
- 2026 only: where organizations measure AI use in performance, 88.1% of users are daily (69.7% where use is optional); among very unfavorable users, 67.6% vs 45.8%.
- All six pre-specified replication criteria were met. The 2023-2025 Likert trust trend cannot be extended to 2026.

## What this does not show

- **Not causal.** The design cannot determine whether stance precedes use, follows experience with use, reflects usefulness or role fit, or partly rationalizes established behavior.
- **Criterion proximity is real.** The stance item asks about *using AI tools as part of your development workflow*, and the outcome is *reported use frequency*. The overlap is genuine and unresolvable within this dataset.
- **Both predictors and outcome are contemporaneous self-reports** from a voluntary survey with no sampling weights. Neither stance nor trust is a validated multi-item scale.
- **Stack Overflow respondents do not represent all developers.**
- **2025-to-2026 level changes cross an instrument redesign.** Direction is defensible; exact magnitudes are not.

## Withdrawn claims

| Withdrawn | Status |
|---|---|
| Five stable developer archetypes exist | Not supported by the clustering diagnostics. Removed. |
| Random-forest Gini share proves stance dominance | Not supported as a standalone inference. Replaced with nested CV and held-out permutation checks. |
| Structured AI learning drives adoption | Not supported by the available learning-route field. Removed. |
| Full-sample endpoint separation proves the main claim | Overstated; the stance item is close to current-use status. Current-user comparison is now primary. |
| Stance causes daily use | Never supported. Do not cite. |

Earlier feature recodes (`AIComplexScore`, `AgentScore`, `LearnedAI`) mixed non-evaluative opt-outs and adoption *intent* into predictors of use. They have been removed from the model in favor of demographic and context controls.

## Reproducing

```bash
pip install -r requirements.txt
# place the Stack Overflow public CSVs at data/<year>/survey_results_public.csv
python analysis/verify_data.py
python analysis/sentiment_deep_dive.py              # 2025 analysis (outputs/sentiment/)
python analysis/sentiment_deep_dive.py --year 2026  # 2026 replication (outputs/sentiment_2026/)
```

Run the 2025 analysis first; the 2026 run reads its stance-gradient table to draw the two-year comparison figure. Seeds are fixed (42). pandas 3.x breaks the pipeline; use the pinned versions.

**Note:** the country-grouped `GroupKFold` step one-hot encodes 173 countries and is memory-hungry — allow several GB of RAM. The rest of the pipeline runs comfortably on a laptop.

Data must be downloaded separately from the StackExchange/Survey GitHub archive (see [`data/README_data.md`](data/README_data.md) for paths and SHA-256 checksums).

## Documentation

- [`docs/METHODS.md`](docs/METHODS.md) — design, samples, specifications, robustness checks
- [`docs/CLAIM_LEDGER.md`](docs/CLAIM_LEDGER.md) — every claim, its evidence status, and the approved language
- [`docs/CODEBOOK.md`](docs/CODEBOOK.md) — variable recodes and decision notes
- [`docs/DENOMINATORS.md`](docs/DENOMINATORS.md) — denominator reconciliation across years
- [`docs/INTAKE_DECISIONS_2026.md`](docs/INTAKE_DECISIONS_2026.md) — 2026 item mapping, routing, pre-specified criteria
- [`docs/FINDINGS_2026.md`](docs/FINDINGS_2026.md) — what changed from 2025 to 2026 and what the data show

## Citation

```
Penzell, J. (2026). Adoption Without Confidence? Favorable Stance, Trust,
and Reported AI-Use Frequency in the 2025 and 2026 Stack Overflow Surveys. Version 3.2.0.
Imagination Applied Open Research Series.
https://github.com/jpenzell/ai-adoption-paradox
```

Data citation:

```
Stack Overflow. (2025, 2026). Stack Overflow Developer Survey.
https://github.com/StackExchange/Survey (packages/archive/<year>)
```

## Contact

Josh Penzell · Imagination Applied · <https://joshpenzell.com>
