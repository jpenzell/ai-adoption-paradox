# AI Adoption Paradox: A Repeated Cross-Sectional Analysis of the Stack Overflow Developer Survey (2023–2025)

**Imagination Applied Research Series**

This repository contains the full analysis code, outputs, and documentation for the paper *AI Adoption Paradox: A Repeated Cross-Sectional Analysis of the Stack Overflow Developer Survey, 2023–2025*.

---

## Study Summary

This report analyzes three consecutive years of the Stack Overflow Developer Survey (2023–2025, combined N=203,812) using clustering, association rule mining, and random forest classification to identify AI adoption archetypes and their behavioral and attitudinal correlates.

**Core finding:** AI adoption among surveyed developers rose from 44.4% (2023) to 78.5% (2025). Over the same period, favorable sentiment fell from 76.3% to 59.7% and "highly distrust" rose from 5.5% to 19.6% — a pattern we term the Adoption Paradox. This is a repeated cross-sectional study; comparisons over time describe population-level shifts across independent annual cohorts, not individual-level change.

---

## Repository Structure

```
├── analysis/
│   ├── config.py             # Data path configuration (edit DATA_ROOT here)
│   ├── pipeline_v2.py        # Primary analysis: clustering, RF classification,
│   │                         #   association rules, + robustness checks A–E:
│   │                         #   (A) 3-seed stability  (B) 5-fold CV
│   │                         #   (C) permutation importance  (D) k-modes
│   │                         #   (E) single-method learner analysis
│   ├── longitudinal.py       # Year-over-year trend analysis (2023–2025)
│   ├── deep_dives.py         # Learning methods, frustration, job threat analyses
│   └── carousel_build.py     # LinkedIn carousel figure generation
├── outputs/
│   ├── adoption_paper_v22.docx   # Final manuscript
│   └── infographic_v2.jsx        # Interactive infographic (React)
├── docs/
│   ├── CODEBOOK.md           # Variable recode documentation (all 6 cluster features
│   │                         #   + 8 classification features, with decision notes)
│   └── DENOMINATORS.md       # Denominator reconciliation (2023–2025, with 2023
│                             #   AISelect denominator explained)
├── requirements.txt          # Python dependencies
└── data/
    └── README_data.md        # Data download instructions + SHA-256 checksums
```

---

## Data Access

The Stack Overflow Developer Survey data is publicly available and must be downloaded separately:

| Year | URL | SHA-256 (first 16 chars) | Rows |
|------|-----|--------------------------|------|
| 2025 | https://survey.stackoverflow.co/datasets | `2d1f65308877282e` | 49,191 |
| 2024 | https://survey.stackoverflow.co/datasets | `7f2c2dbf6989d00b` | 65,437 |
| 2023 | https://survey.stackoverflow.co/datasets | `828874a3cf0fa1bb` | 89,184 |

Download the CSV files and place them at:
```
data/2025/survey_results_public.csv
data/2024/survey_results_public.csv
data/2023/survey_results_public.csv
```

This matches the path convention in `analysis/config.py`. If you want to store the data elsewhere, edit the `DATA_ROOT` variable in that file.

---

## Reproducing the Analysis

### Requirements

```bash
pip install pandas numpy scikit-learn matplotlib seaborn mlxtend kmodes
```

### Run order

```bash
# Run from the repo root directory
cd ai-adoption-paradox

# 1. Verify data files are in place
python -c "from analysis.config import check_data; check_data()"

# 2. Primary clustering, classification, and association rules (2025)
python analysis/pipeline_v2.py

# 3. Year-over-year comparisons across 2023–2025
python analysis/longitudinal.py

# 4. Deep-dive analyses (learning methods, frustrations, job threat)
python analysis/deep_dives.py
```

All random seeds are fixed (seed=42 throughout). Scripts import data paths from `analysis/config.py` — edit `DATA_ROOT` there if your data lives elsewhere.

---

## Key Analytical Decisions

See `docs/CODEBOOK.md` for full recode documentation. Three decisions warrant particular attention:

1. **AIComplexScore**: The response "I don't use AI tools for complex tasks / I don't know" was mapped to 2 (same as "Neither good nor bad"). This conflates a non-evaluative opt-out with a neutral rating (n=5,582 affected). Researchers may prefer to treat this as missing.

2. **AgentScore**: "No, but I plan to" (non-user) was grouped with infrequent users at score=1. This treats adoption intent as equivalent to infrequent use.

3. **2025 trust denominator**: The 2025 trust question (AIAcc) was routed to all AISelect respondents including non-users, while 2023/2024 were routed to current users only. The paper reports both the full-denominator figures (32.8% high trust) and the harmonized user-only figure (39.3% high trust, n=26,126). See `docs/DENOMINATORS.md`.

---

## Citation

If you use this analysis, please cite:

```
Penzell, J. (2025). AI Adoption Paradox: A Repeated Cross-Sectional Analysis of the
Stack Overflow Developer Survey, 2023–2025. Imagination Applied Research Series.
[INSERT REPOSITORY URL BEFORE PUBLISHING]
```

Data citation:
```
Stack Overflow. (2023, 2024, 2025). Stack Overflow Developer Survey.
https://survey.stackoverflow.co/datasets
```

---

## Contact

Josh Penzell | Imagination Applied | [imaginationapplied.com]
