# Codebook: Variable Recode Documentation

All recodes below were applied before model fitting and held constant throughout. This file documents every collapsed mapping decision so the analysis can be exactly reproduced.

---

## AIUsageScore (0–4)
**Source column:** `AISelect`  
**Official question:** "Do you currently use AI tools in your development process?"

| Survey Response | Score |
|---|---|
| Yes, I use AI tools daily | 4 |
| Yes, I use AI tools weekly | 3 |
| Yes, I use AI tools monthly or infrequently | 2 |
| No, but I plan to soon | 1 |
| No, and I don't plan to | 0 |

**Missing:** Excluded from clustering sample (used as required feature).

---

## AITrustScore (0–4)
**Source column:** `AIAcc` (2024–2025), `AIBen` (2023)  
**Official question:** "How much do you trust the accuracy of the output from AI tools as part of your development workflow?"

| Survey Response | Score |
|---|---|
| Highly trust | 4 |
| Somewhat trust | 3 |
| Neither trust nor distrust | 2 |
| Somewhat distrust | 1 |
| Highly distrust | 0 |

**Missing:** Excluded from clustering sample (used as required feature).

**⚠ Denominator note (2025):** In 2023 and 2024, this question was routed to current AI users only. In 2025, it was routed to all AISelect respondents including non-users. Non-users show substantially lower trust (8.9% high trust vs. 39.3% for current users). Both the full-denominator and user-only figures are reported in the paper. See DENOMINATORS.md.

---

## AISentScore (0–5)
**Source column:** `AISent`  
**Official question:** "How favorable is your stance on using AI tools as part of your development workflow?"

| Survey Response | Score |
|---|---|
| Very favorable | 5 |
| Favorable | 4 |
| Indifferent | 3 |
| Unsure | 2 |
| Unfavorable | 1 |
| Very unfavorable | 0 |

**Missing:** Excluded from clustering sample (used as required feature).

---

## AIComplexScore (0–5)
**Source column:** `AIComplex`  
**Official question:** "How well do the AI tools you use handle complex tasks?"

| Survey Response | Score | Note |
|---|---|---|
| Very well at handling complex tasks | 5 | |
| Good, but not great at handling complex tasks | 4 | |
| Neither good or bad at handling complex tasks | 3 | |
| I don't use AI tools for complex tasks / I don't know | 2 | ⚠ See note below |
| Bad at handling complex tasks | 1 | |
| Very poor at handling complex tasks | 0 | |

**⚠ Important:** "I don't use AI tools for complex tasks / I don't know" is a non-evaluative opt-out, not a rating. It was mapped to 2 (same numeric value as "Neither good nor bad") in this analysis. This affects n=5,582 respondents (16.8% of AIComplex respondents). Researchers replicating this work may prefer to recode these as NaN and impute separately.

**Missing (after above recode):** Imputed with column median (3). Affected n ≈ 1,609 in clustering sample.

---

## AgentScore (0–2)
**Source column:** `AIAgents`  
**Official question:** "Are you using AI agents in your work (development or otherwise)? AI agents refer to autonomous software entities that can operate with minimal to no direct human intervention using artificial intelligence techniques."

| Survey Response | Score | Note |
|---|---|---|
| Yes, I use AI agents at work daily | 2 | |
| Yes, I use AI agents at work weekly | 2 | |
| Yes, I use AI agents at work monthly or infrequently | 1 | |
| No, but I plan to | 1 | ⚠ See note below |
| No, I use AI exclusively in copilot/autocomplete mode | 0 | |
| No, and I don't plan to | 0 | |

**⚠ Note:** "No, but I plan to" (non-user) is grouped with "monthly or infrequently" (actual user) at score=1. This treats adoption intent as equivalent to infrequent use, which is a debatable conflation.

**Missing:** Imputed with column median (0). Affected n ≈ 1,312 in clustering sample.

---

## LearnedAI (0/1)
**Source column:** `LearnCodeAI`  
**Official question:** "Did you spend time in the last year learning AI programming or AI-enabled tooling on your own or at work?"

| Survey Response | Code |
|---|---|
| Yes, I learned how to use AI-enabled tools for my personal curiosity and/or hobbies | 1 |
| Yes, I learned how to use AI-enabled tools required for my job or to benefit my career | 1 |
| No, I learned something that was not related to AI or AI enablement for my personal curiosity and/or hobbies | 0 |
| No, I learned something that was not related to AI or AI enablement as required for my job or to benefit my career | 0 |
| No, I didn't spend time learning in the past year | 0 |

**Missing:** Coded as 0. Affected n ≈ 489 in clustering sample.

---

## Clustering Sample Construction

The working sample (n=33,231) was constructed as follows:

1. Start with all AISelect respondents in 2025 CSV: **n=33,720**
2. Require non-missing AIUsageScore, AITrustScore, AISentScore: **n=33,231** (489 excluded)
3. Impute AgentScore NAs with column median (0): **1,312 respondents imputed**
4. Impute AIComplexScore NAs with column median (3): **1,609 respondents imputed**
5. Code LearnedAI NAs as 0: **489 respondents recoded**

This sample is **not** "complete AI module data." Other AI module questions have lower response counts:
- AIAgents: 31,919 non-missing in CSV (vs. 31,877 on SO public page)
- AI Frustrations (AIFrustration): 31,476 non-missing
- AILearnHow (learning method): 28,172 non-missing

---

## Classification Features (8 core features)

The Random Forest and Decision Tree classifiers use the following 8 features, all drawn from the 2025 survey. The full clustering sample (n=33,231) is used; missing values in all features are median-imputed before fitting.

| Feature | Source | Type | Notes |
|---|---|---|---|
| AISentScore | AISent | Ordinal 0–5 | Strongest predictor by both Gini and permutation importance |
| AgentScore | AIAgents | Ordinal 0–2 (collapsed) | See recode table above |
| LearnedAI | LearnCodeAI | Binary 0/1 | |
| AITrustScore | AIAcc | Ordinal 0–4 | |
| AIComplexScore | AIComplex | Ordinal 0–5 (collapsed) | See recode note above |
| ThreatScore | AIThreat | Binary 0/1 | Yes=1; No=0; "I'm not sure"=0. Note: "unsure" is deliberately collapsed into 0 (not threatened). This treats ambivalence as non-threatening. Researchers preferring a 3-category encoding should recode before fitting. |
| WorkExp | WorkExp | Numeric (years) | Median-imputed where missing |
| YearsCode | YearsCode | Numeric (years) | Median-imputed where missing |

Target: `daily_adopter` = 1 if AIUsageScore == 4, else 0 (47.1% positive class).

**Note on earlier manuscript versions:** A 13-feature setup including OrgSize, DevType, Country, and YearsCodePro was explored in development but the released pipeline uses the 8 features above.
