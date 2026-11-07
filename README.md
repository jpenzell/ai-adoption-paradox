# Adoption Without Confidence?

**Favorable stance, trust, and reported AI-use frequency in the 2025 and 2026 Stack Overflow surveys**

Josh Penzell · Imagination Applied Open Research Series · November 2026

This repository contains a secondary analysis of AI-use frequency, attitude and trust in the 2025 and 2026 Stack Overflow Developer Surveys. It examines whether attitude and trust carry different information about daily use among current AI users. The two years are analyzed separately because the survey redesigned all three core measures in 2026. See [`docs/RELEASE_AUDIT.md`](docs/RELEASE_AUDIT.md) for verification scope and limitations.

## Main finding

Among current AI users with complete core answers in the 2026 analysis, **54.3%** of those with a very unfavorable attitude report daily use on at least one of four tool types; **93.0%** of very favorable users do so. There remains a strong relationship between stance and frequency, but usage alone cannot substitute for directly asking about attitude or reliance.

The 2025 endpoints are **18.8%** and **88.1%**. All three core questions changed in 2026, as did routing and aspects of survey collection. Treat these as separate cross-sections, not a clean measure of behavioral change or proof that its direction is unaffected by measurement.

| Within-year result | 2025 | 2026 |
|---|---:|---:|
| Current-user primary sample | 26,102 | 14,158 |
| Daily numerator | 15,648 | 10,789 |
| Daily share | 59.9% | 76.2% |
| Stance-only fivefold ROC AUC | 0.758 | 0.722 |
| Trust-only fivefold ROC AUC | 0.669 | 0.657 |
| Context+stance fivefold ROC AUC | 0.790 | 0.761 |
| Context+trust fivefold ROC AUC | 0.704 | 0.713 |
| Context+stance outperforms context+trust | 50/50 repeated folds | 50/50 repeated folds |

2025 daily use is one overall development-process item. 2026 daily use is the maximum across four tool-type questions about work. Coding-assistant daily use is 73.6% **among 11,246 respondents answering coding-assistant frequency**, a different denominator. Trust measures accuracy in 2025 and reliance scope in 2026; the old trust trend cannot be extended.

These are voluntary, unweighted, contemporaneous self-reports. Neither causality nor population representativeness is established. The repeated folds overlap; they are not 50 independent studies. Exploratory organizational-policy differences are associations, not evidence that policies produce use or resentment.

## Reproducing

Python 3.10+ is required. From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analysis/fetch_data.py
python analysis/verify_data.py
python analysis/sentiment_deep_dive.py
python analysis/sentiment_deep_dive.py --year 2026
python analysis/exploratory_2026.py
```

The portable downloader checks the package-specified SHA-256 before installing each input. It preserves existing mismatched files unless `--replace` is explicitly supplied. Raw files are not bundled. URLs use the source repository's current branch, while fixed hashes enforce the input identity recorded by the package. If a URL or hash fails, stop and resolve the source discrepancy; do not silently analyze a changed file.

Run 2025 before 2026 because the two-year chart reads the earlier stance table. Main fivefold CV, held-out split and permutation importance use seed 42; repeated fivefold CV uses seed 719. Preprocessing happens inside training folds. pandas and scikit-learn are pinned; other version ranges may introduce minor numerical/rendering differences. Use floating-point tolerances rather than promising all output bytes are identical. Allow several GB of memory for country encoding and parallel validation.

## Documentation and evidence

- [`docs/METHODS.md`](docs/METHODS.md): design, models, validation and limitations
- [`docs/CODEBOOK.md`](docs/CODEBOOK.md): actual current recodes
- [`docs/DENOMINATORS.md`](docs/DENOMINATORS.md): counts and denominator distinctions
- [`docs/INTAKE_DECISIONS_2026.md`](docs/INTAKE_DECISIONS_2026.md): supplied mapping and criteria
- [`docs/FINDINGS_2026.md`](docs/FINDINGS_2026.md): supported results and interpretation
- [`docs/CLAIM_LEDGER.md`](docs/CLAIM_LEDGER.md): defensible and unsupported claims
- [`docs/RELEASE_AUDIT.md`](docs/RELEASE_AUDIT.md): what this revision did and did not verify
- [`data/README_data.md`](data/README_data.md): input URLs/hashes inherited from the package

Earlier clustering, archetype, random-forest Gini-importance and structured-learning claims are withdrawn. They are not part of the current logistic analysis.

## Attribution

Proposed study citation: Penzell, J. (2026). *Adoption Without Confidence? Favorable Stance, Trust, and Reported AI-Use Frequency in the 2025 and 2026 Stack Overflow Surveys.* Imagination Applied Open Research Series. Publication status and final URL must be verified when released.

Data: Stack Overflow Developer Survey, 2023–2026, under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/); individual cell contents under [DbCL 1.0](https://opendatacommons.org/licenses/dbcl/1-0/). Source and attribution: [StackExchange/Survey](https://github.com/StackExchange/Survey#license-and-data-attribution). This analysis is independent of Stack Overflow.
