# Adoption Without Confidence?

**Favorable Stance, Accuracy Trust, and Reported AI-Use Frequency in the 2025 Stack Overflow Survey**

Josh Penzell · Imagination Applied Open Research Series · **v3.1.0 (2026)**

---

> ### ⚠️ This repository was substantially revised in 2026
>
> Commits before v3.1.0 contained an earlier analysis titled *"Human–AI Work Patterns in Software Development: Archetypes, Paradoxes, and the Decline of Trust,"* built on k-means/k-modes clustering, association rule mining, and random-forest Gini importance.
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

## What this does not show

- **Not causal.** The design cannot determine whether stance precedes use, follows experience with use, reflects usefulness or role fit, or partly rationalizes established behavior.
- **Criterion proximity is real.** The stance item asks about *using AI tools as part of your development workflow*, and the outcome is *reported use frequency*. The overlap is genuine and unresolvable within this dataset.
- **Both predictors and outcome are contemporaneous self-reports** from a voluntary survey with no sampling weights. Neither stance nor trust is a validated multi-item scale.
- **Stack Overflow respondents do not represent all developers.**

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
python analysis/sentiment_deep_dive.py
```

Seeds are fixed (42). Outputs are written to `outputs/sentiment/`.

**Note:** the country-grouped `GroupKFold` step one-hot encodes 173 countries and is memory-hungry — allow several GB of RAM. The rest of the pipeline runs comfortably on a laptop.

Data must be downloaded separately from <https://survey.stackoverflow.co/datasets>. SHA-256 checksums are in [`data/README_data.md`](data/README_data.md).

## Documentation

- [`docs/METHODS.md`](docs/METHODS.md) — design, samples, specifications, robustness checks
- [`docs/CLAIM_LEDGER.md`](docs/CLAIM_LEDGER.md) — every claim, its evidence status, and the approved language
- [`docs/CODEBOOK.md`](docs/CODEBOOK.md) — variable recodes and decision notes
- [`docs/DENOMINATORS.md`](docs/DENOMINATORS.md) — denominator reconciliation across years

## Citation

```
Penzell, J. (2026). Adoption Without Confidence? Favorable Stance, Accuracy Trust,
and Reported AI-Use Frequency in the 2025 Stack Overflow Survey. Version 3.1.0.
Imagination Applied Open Research Series.
https://github.com/jpenzell/ai-adoption-paradox
```

Data citation:

```
Stack Overflow. (2025). Stack Overflow Developer Survey.
https://survey.stackoverflow.co/datasets
```

## Contact

Josh Penzell · Imagination Applied · <https://joshpenzell.com>
