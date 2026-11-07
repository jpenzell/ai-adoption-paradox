# Findings: the 2026 update

**Adoption Without Confidence?** v3.2.0 (November 2026). Companion to
[`INTAKE_DECISIONS_2026.md`](INTAKE_DECISIONS_2026.md) (what was mapped and
why) and [`METHODS.md`](METHODS.md). All numbers below are in
`outputs/sentiment_2026/` and `outputs/sentiment/` and were produced by
`analysis/sentiment_deep_dive.py --year 2026` and the unchanged 2025 run.

## One paragraph

In 2025, the most unfavorable AI users were mostly not daily users: 18.8%
of "very unfavorable" current users reported daily use, against 88.1% of
"very favorable" users. In 2026, on a redesigned survey, the floor rose to
54.3% while the ceiling rose to 93.0%. Daily use among all current users went
from 60.0% to 76.2%. Favorable stance among users kept falling, from 85% in
2023 to 62% in 2026, and the unfavorable share more than doubled to 21%.
Stance still carries more information about reported daily use than trust
does (AUC 0.722 vs 0.657; 50 of 50 matched splits), but the gap narrowed
from 0.087 to 0.048, and Stack Overflow's new reliance-scope trust question
adds more incremental information than the old accuracy question did. The
2026 data also show that where organizations measure AI use in performance
reviews, even very unfavorable users are mostly daily users (67.6%, vs 45.8%
where use is optional). None of this is causal. The one-line reading: daily
AI use has become something developers do whether or not they like it.

## What changed, 2025 to 2026

| | 2025 | 2026 | Note |
|---|---|---|---|
| Public CSV rows | 49,191 | 30,903 | New validity rules in 2026 |
| Answered the AI-use item | 33,720 | 17,290 | 2026 routes far fewer respondents to the AI module |
| Current users, complete case (primary sample) | 26,102 | 14,158 | 2026 stance and trust routed to users only |
| Professional share of primary sample | 79.5% | 80.1% | `MainBranch` vs `CodeMain` |
| Daily use among current users | 60.0% | 76.2% | 2026 = daily on any of four tool types; coding assistants alone 73.6%, chat tools alone 66.3% |
| Daily use, very unfavorable users | 18.8% (n=585) | 54.3% (n=958) | +35.5 points |
| Daily use, unfavorable | 20.1% (n=1,928) | 55.7% (n=2,052) | |
| Daily use, unsure | 34.0% (n=288) | 70.4% (n=159) | small n both years |
| Daily use, indifferent / neutral | 31.5% (n=4,353) | 63.5% (n=2,156) | unsure > indifferent reversal persists |
| Daily use, favorable / somewhat favorable | 62.0% (n=11,540) | 79.9% (n=4,321) | |
| Daily use, very favorable | 88.1% (n=7,408) | 93.0% (n=4,512) | +4.9 points |
| Gradient (very favorable minus very unfavorable) | 69.3 points | 38.7 points | compressed by 30 points |
| Stance-only CV AUC | 0.758 | 0.722 | |
| Trust-only CV AUC | 0.669 | 0.657 | different trust item |
| Context-only CV AUC | 0.627 | 0.638 | 2026 drops AIThreat |
| Context + trust | 0.704 | 0.713 | |
| Context + stance | 0.790 | 0.761 | |
| Context + trust + stance | 0.793 | 0.774 | |
| Stance-over-trust advantage (50 matched splits, mean AUC delta) | +0.087, 50/50 | +0.048, 50/50 | narrowed |
| Trust increment over context + stance | +0.003, 50/50 | +0.012, 50/50 | new item carries more |
| Held-out AUC / calibration slope | 0.789 / 0.96 | 0.772 / 0.91 | |
| Country-grouped AUC, stance / trust / full | 0.756 / 0.665 / 0.789 (173 countries) | 0.721 / 0.656 / 0.769 (157 countries) | ordering holds |
| Professional-only, stance / trust | 0.763 / 0.675 | 0.740 / 0.672 | ordering holds |
| Permutation importance, held-out: stance / trust | 0.219 / 0.006 | 0.149 / 0.038 | trust's share rose sixfold |

## What the data show

### 1. The floor rose

Among current users who describe their attitude toward AI at work as very
unfavorable, 54.3% now report daily use on at least one AI tool type. On
coding assistants alone the figure is 58.5%; on general chat tools alone,
47.7%. In 2025 the equivalent group was 18.8%. The measurement changed, but
every sensitivity version of the 2026 outcome lands far above the 2025
figure. Among the favorable the change is small because there was little
headroom: 88.1% to 93.0%.

The paper's title question was whether adoption was happening without
confidence. In 2025 it was happening mostly among people who at least said
they were favorable. In 2026 it is happening among the unfavorable too.

### 2. The stance gradient survived the redesign, flatter

Stance remains the strongest single item for separating daily from
less-frequent use. Every pre-specified replication criterion was met
(INTAKE_DECISIONS_2026.md). But the gradient compressed from 69 points to 39,
and the stance-only AUC fell from 0.758 to 0.722. The two readings are not in
conflict: when three-quarters of users are daily, there is less variation for
any item to explain, and the floor rose faster than the ceiling.

### 3. Trust was re-asked as reliance scope, and it matters more that way

Stack Overflow replaced the five-point accuracy-trust Likert with six
reliance-scope options. Among 2026 current users: 48.2% trust the output when
they can easily verify it; 16.4% trust it for many tasks but not important
decisions; 16.2% trust it for low-risk tasks only; 12.1% do not trust it for
most work tasks; 6.7% trust it including important decisions; 0.5% not sure.

The reliance item is still a weaker separator of daily use than stance
(0.657 vs 0.722), but it carries more incremental information once stance
and context are in the model (+0.012 AUC vs +0.003 for the old item), and its
held-out permutation importance is six times what the accuracy item had in
2025. The old question asked whether people believed the output; the new one
asks what they are willing to hand to it. The second is closer to behavior.

The 2023-2025 Likert trust trend (48.2% trusting among users in 2023, 43.0%
in 2024, 39.3% in 2025) stops at 2025. It cannot be extended with the 2026
item.

### 4. Favorable stance kept falling

Using the current-user denominator in every year: favorable or very
favorable was 84.8% of users in 2023, 76.8% in 2024, 72.6% in 2025, and 62.3%
in 2026. Unfavorable or very unfavorable: 2.3%, 5.7%, 9.6%, 21.2%. The 2026
labels add "somewhat" to the middle options, which may pull some respondents
toward the poles, so the size of the 2026 step is not clean. The direction
is consistent with the three prior years and with Stack Overflow's own
reporting.

### 5. Within daily users, stance does not sort heavy from light use

Among daily users, 31.2% report four or more hours of AI use per workday.
Stance and trust are nearly equal and weak at separating these heavy users
from other daily users (AUC 0.653 and 0.644); context adds more than either
(full model 0.732). The relationship is not monotone: 46.0% of very
favorable daily users are at four-plus hours, 23.2% of favorable, 18.3% of
indifferent, 16.2% of unfavorable, and then 31.2% of very unfavorable. The
most negative daily users are heavier users than the mildly negative ones.
This is an observation, not an explanation; both "heavy exposure sours
people" and "mandated heavy use is resented" are consistent with it, and so
is role mix.

### 6. Organizational policy tracks daily use, including among the unfavorable

A 2026-only item asks how AI is used at the respondent's organization. Daily
use among current users, by policy: optional and left to individuals 69.7%
(n=3,261); encouraged but varies by team 78.0%; approved tools and guidance
80.0%; expected for some work 82.5%; measured or evaluated in performance
88.1% (n=1,259). Among very unfavorable users the same ordering appears:
45.8% daily where use is optional, 67.6% where it is measured. Very
unfavorable users are also somewhat over-represented in organizations that
measure AI use (18.9% of them sit in such organizations, against about 11%
of favorable users). This is a cross-sectional association from a voluntary
survey and cannot say whether measurement produces use, resentment, or
both.

## Exploratory cuts (not pre-specified)

Run by `analysis/exploratory_2026.py`; tables in
`outputs/sentiment_2026/exploratory_*.csv`. These were chosen after seeing
the main results, to test readings of the floor-rise finding. Treat them as
hypotheses for the 2027 survey, not findings.

**Do unfavorable users expect to pull back?** Only partly. Asked which
workflow parts they expect to use AI more or less for next year, 50% of very
unfavorable users name at least one part where they expect less (31% of very
favorable). But 68% of very unfavorable users also name at least one part
where they expect more, and they name twice as many "more" parts as "less"
parts (3.6 vs 1.8). Resistance shows up as scope limitation (6.5 workflow
parts they do not plan to use, against 1.5 for the very favorable), not
withdrawal. Among daily users specifically, the very unfavorable are no more
likely to expect less (43%) than the favorable (44%); the group most likely to
expect less is the mildly unfavorable and indifferent (53%).

**Control over what the AI sees.** Very unfavorable users are less likely to
say they decide exactly what information the tool gets (47% vs 53% of very
favorable) and three times as likely to say they are not sure what it uses
(11% vs 4%). Perceived loss of control travels with negative stance.

**Verification behavior cuts the other way.** Asked what they do before using
AI output, very favorable users are twice as likely to use it as-is (15% vs
7% for the unfavorable), less likely to read official docs (28% vs 46%), and
much less likely to search Stack Overflow (7% vs 17%). They run it locally
more (80% vs 66%). The enthusiasts verify by execution; the skeptics verify
by reading. "Unsure" users are the other as-is group (17%, n=140).

**Job satisfaction.** Mean satisfaction (0-10) runs 6.1 for very unfavorable
to 7.5 for very favorable; 24% of the very unfavorable score 0-4 against 7%
of the very favorable. Among those who feel complacent, "AI automating the
challenging parts of my job" is named by 16% of very unfavorable users and
9% of very favorable. These are modest associations in a cross-section and
say nothing about direction.

## What this does not show

Unchanged from v3.1.0, with two additions.

- Not causal. The design cannot say whether stance precedes use or follows
  it, in either year.
- Criterion proximity remains. The stance item asks about using AI tools at
  work; the outcome is reported use frequency.
- Contemporaneous self-reports from a voluntary, unweighted survey. Stack
  Overflow respondents do not represent all developers, and the 2026
  respondent pool is 37% smaller than 2025's with new validity rules.
- **New:** the 2025-to-2026 comparison crosses an instrument redesign on all
  three core items. Level changes (especially daily share and the stance
  distribution) are partly measurement. The within-year replication of the
  stance-over-trust ordering is the defensible cross-year claim; exact
  magnitudes are not.
- **New:** the 2026 trust item is nominal. "Trust" in 2026 results means
  reliance scope, not belief in accuracy.

## Language that is and is not supported

See [`CLAIM_LEDGER.md`](CLAIM_LEDGER.md), 2026 rows.
