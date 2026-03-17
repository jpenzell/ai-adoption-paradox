"""
Human–AI Work Patterns: Longitudinal Analysis
Stack Overflow Developer Survey — 2023 · 2024 · 2025

Comparable signals across years:
  - AISelect  → Adoption rate       (all 3 years; question wording changed in 2025)
  - AISent    → Sentiment           (all 3 years; identical scale)
  - Trust     → AIBen(2023) / AIAcc(2024-25); same Likert scale, column renamed
  - AIThreat  → Job threat          (2024-2025 only)
  - AIComplex → Complexity rating   (2024-2025 only)
  - AITool*   → Task usage          (all 3 years; normalized task labels)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')

from config import CSV_2023, CSV_2024, CSV_2025, check_data
check_data()

sns.set_theme(style="whitegrid")
PALETTE = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B2"]
YEARS = [2023, 2024, 2025]
YEAR_COLORS = {"2023": "#8172B2", "2024": "#4C72B0", "2025": "#DD8452"}
plt.rcParams['figure.dpi'] = 130

print("=" * 70)
print("  LONGITUDINAL ANALYSIS — 2023 · 2024 · 2025")
print("=" * 70)

# ─── LOAD ─────────────────────────────────────────────────────────────────────
print("\n[1] Loading data...")
df23 = pd.read_csv(CSV_2023, low_memory=False)
df24 = pd.read_csv(CSV_2024, low_memory=False)
df25 = pd.read_csv(CSV_2025, low_memory=False)

print(f"    2023: {len(df23):,} respondents")
print(f"    2024: {len(df24):,} respondents")
print(f"    2025: {len(df25):,} respondents")

# ─── METRIC 1: ADOPTION RATE ──────────────────────────────────────────────────
print("\n[2] Computing adoption rates...")

# 2023/2024: "Yes" vs "No, but plan to" vs "No, and don't plan to"
def adoption_rate_old(df):
    vc = df['AISelect'].value_counts()
    total = vc.sum()
    using = vc.get('Yes', 0)
    planning = vc.get('No, but I plan to soon', 0)
    return {
        'currently_using': using / total,
        'planning': planning / total,
        'not_planning': 1 - (using + planning) / total,
        'n': total
    }

# 2025: granular frequency breakdown
def adoption_rate_2025(df):
    vc = df['AISelect'].value_counts()
    total = vc.sum()
    daily   = vc.get('Yes, I use AI tools daily', 0)
    weekly  = vc.get('Yes, I use AI tools weekly', 0)
    monthly = vc.get('Yes, I use AI tools monthly or infrequently', 0)
    plan    = vc.get('No, but I plan to soon', 0)
    no      = vc.get("No, and I don't plan to", 0)
    return {
        'currently_using': (daily + weekly + monthly) / total,
        'planning': plan / total,
        'not_planning': no / total,
        'daily': daily / total,
        'weekly': weekly / total,
        'monthly': monthly / total,
        'n': total
    }

a23 = adoption_rate_old(df23)
a24 = adoption_rate_old(df24)
a25 = adoption_rate_2025(df25)

print(f"    2023: {a23['currently_using']:.1%} currently using  |  n={a23['n']:,}")
print(f"    2024: {a24['currently_using']:.1%} currently using  |  n={a24['n']:,}")
print(f"    2025: {a25['currently_using']:.1%} currently using  |  n={a25['n']:,}")
print(f"           (of which: {a25['daily']:.1%} daily, {a25['weekly']:.1%} weekly, {a25['monthly']:.1%} monthly)")

# ─── METRIC 2: SENTIMENT ──────────────────────────────────────────────────────
print("\n[3] Computing sentiment trends...")

def sentiment_dist(df, col='AISent'):
    vc = df[col].value_counts()
    total = vc.sum()
    pos  = (vc.get('Very favorable',0) + vc.get('Favorable',0)) / total
    neu  = (vc.get('Indifferent',0)   + vc.get('Unsure',0))     / total
    neg  = (vc.get('Very unfavorable',0) + vc.get('Unfavorable',0)) / total
    v_pos = vc.get('Very favorable',0) / total
    v_neg = vc.get('Very unfavorable',0) / total
    return {'positive': pos, 'neutral': neu, 'negative': neg,
            'very_positive': v_pos, 'very_negative': v_neg, 'n': total}

s23 = sentiment_dist(df23)
s24 = sentiment_dist(df24)
s25 = sentiment_dist(df25)

for yr, s in [('2023',s23),('2024',s24),('2025',s25)]:
    print(f"    {yr}: +{s['positive']:.1%} positive  |  {s['neutral']:.1%} neutral  |  -{s['negative']:.1%} negative  (n={s['n']:,})")

# ─── METRIC 3: TRUST ──────────────────────────────────────────────────────────
print("\n[4] Computing trust trends...")

# 2023 uses AIBen for trust, 2024-2025 uses AIAcc — same Likert options
def trust_dist(df, col):
    vc = df[col].value_counts()
    # Only rows matching trust scale
    scale = ['Highly trust','Somewhat trust','Neither trust nor distrust',
             'Somewhat distrust','Highly distrust']
    vc_t = vc[vc.index.isin(scale)]
    total = vc_t.sum()
    if total == 0: return None
    high  = (vc_t.get('Highly trust',0) + vc_t.get('Somewhat trust',0)) / total
    neu   = vc_t.get('Neither trust nor distrust',0) / total
    low   = (vc_t.get('Highly distrust',0) + vc_t.get('Somewhat distrust',0)) / total
    high_only = vc_t.get('Highly trust',0) / total
    low_only  = vc_t.get('Highly distrust',0) / total
    return {'high': high, 'neutral': neu, 'low': low,
            'highly_trust': high_only, 'highly_distrust': low_only, 'n': total}

t23 = trust_dist(df23, 'AIBen')   # 2023: trust was in AIBen
t24 = trust_dist(df24, 'AIAcc')
t25 = trust_dist(df25, 'AIAcc')

for yr, t in [('2023',t23),('2024',t24),('2025',t25)]:
    if t:
        print(f"    {yr}: {t['high']:.1%} trust  |  {t['neutral']:.1%} neutral  |  {t['low']:.1%} distrust  (n={t['n']:,})")


# ─── METRIC 3b: HARMONIZED 2025 TRUST (user-only, routing-comparable to 2023/2024) ─────
# Routing note: 2023/2024 routed AIAcc/AIBen to current AI users only.
# 2025 routed to ALL AISelect respondents (including non-users → much lower trust).
# Primary year-over-year comparison must restrict 2025 to current users.
current_users_2025 = df25[df25['AISelect'].str.contains('Yes, I use AI', na=False)]
n_harm = len(current_users_2025)
t25_harm = trust_dist(current_users_2025, 'AIAcc')
if t25_harm:
    print(f"\n[4b] 2025 harmonized trust (current users only, n={n_harm:,} — routing-comparable):")
    print(f"     High trust:    {t25_harm['high']:.1%}  (vs 43.0% in 2024  → primary year-over-year comparison)")
    print(f"     High distrust: {t25_harm['low']:.1%}  (vs 30.4% in 2024)")
    print(f"     Highly distrust: {t25_harm['highly_distrust']:.1%}")
    print(f"     (Full-denom 2025 figures include non-users and are not directly comparable to 2023/2024)")

# ─── METRIC 4: THREAT PERCEPTION (2024-2025) ──────────────────────────────────
print("\n[5] Computing threat perception (2024-2025)...")

def threat_dist(df):
    vc = df['AIThreat'].value_counts()
    total = vc.sum()
    return {
        'yes': vc.get('Yes',0) / total,
        'no': vc.get('No',0) / total,
        'unsure': vc.get("I'm not sure",0) / total,
        'n': total
    }

th24 = threat_dist(df24)
th25 = threat_dist(df25)
print(f"    2024: {th24['yes']:.1%} feel threatened  |  {th24['no']:.1%} no  |  {th24['unsure']:.1%} unsure  (n={th24['n']:,})")
print(f"    2025: {th25['yes']:.1%} feel threatened  |  {th25['no']:.1%} no  |  {th25['unsure']:.1%} unsure  (n={th25['n']:,})")

# ─── METRIC 5: TASK ADOPTION ──────────────────────────────────────────────────
print("\n[6] Computing task usage trends...")

# Normalize task labels across years
TASK_NORMALIZE = {
    'Writing code': 'Writing Code',
    'Debugging and getting help': 'Debugging/Fixing Code',
    'Debugging or fixing code': 'Debugging/Fixing Code',
    'Documenting code': 'Documenting Code',
    'Learning about a codebase': 'Learning Codebase',
    'Testing code': 'Testing Code',
    'Project planning': 'Project Planning',
    'Generating content or synthetic data': 'Generating Content',
    'Search for answers': 'Search for Answers',
    'Committing and reviewing code': 'Code Review',
    'Deployment and monitoring': 'Deployment/Monitoring',
    'Predictive analytics': 'Predictive Analytics',
    'Learning new concepts or technologies': 'Learning Concepts',
    'Creating or maintaining documentation': 'Documenting Code',
}

def task_pct(df, col, total_respondents):
    if col not in df.columns: return {}
    tasks = df[col].dropna().str.split(';').explode().str.strip()
    tasks = tasks.map(TASK_NORMALIZE).dropna()
    vc = tasks.value_counts()
    return (vc / total_respondents).to_dict()

# 2023 and 2024 use single "currently using" column
# AISelect-answered denominator (not all respondents) — matches manuscript Table 4
n23_aiselect = df23['AISelect'].notna().sum()  # 87,973
t23_tasks = task_pct(df23, 'AIToolCurrently Using', n23_aiselect)
n24_aiselect = df24['AISelect'].notna().sum()  # 60,907
t24_tasks = task_pct(df24, 'AIToolCurrently Using', n24_aiselect)

# 2025: respondent-level union of "mostly AI" and "partially AI" columns
# This avoids double-counting respondents who appear in both columns for the same task.
# Implementation: for each respondent, collect the set of tasks from BOTH columns,
# then count unique respondents per task.
def task_union_2025(df, norm_map, total_n):
    """Compute respondent-level task union from two 2025 columns."""
    mostly_col  = 'AIToolCurrently mostly AI'
    partial_col = 'AIToolCurrently partially AI'
    task_respondents = {}  # task_label -> set of respondent indices

    for col in [mostly_col, partial_col]:
        if col not in df.columns:
            continue
        for idx, val in df[col].dropna().items():
            for raw_task in str(val).split(';'):
                normalized = norm_map.get(raw_task.strip(), None)
                if normalized:
                    task_respondents.setdefault(normalized, set()).add(idx)

    return {task: len(indices) / total_n for task, indices in task_respondents.items()}

n25_aiselect = df25['AISelect'].notna().sum()  # 33,720
t25_tasks = task_union_2025(df25, TASK_NORMALIZE, n25_aiselect)

# Documenting Code note: 2025 has two label variants:
#   "Documenting code" (legacy, n=9,815) and
#   "Creating or maintaining documentation" (new, n=8,523).
# Both are normalized to "Documenting Code". Respondents selecting both: n=7,061.
# Respondent-level union: n=11,277 = 33.4% of AISelect respondents (87,973/60,907/33,720 denominators).

CORE_TASKS = ['Writing Code','Debugging/Fixing Code','Documenting Code',
              'Testing Code','Learning Codebase','Project Planning',
              'Search for Answers','Generating Content','Code Review']

print("    Task      2023    2024    2025")
print("    " + "-"*50)
for task in CORE_TASKS:
    p23 = t23_tasks.get(task, 0)
    p24 = t24_tasks.get(task, 0)
    p25 = t25_tasks.get(task, 0)
    print(f"    {task:<28} {p23:.1%}   {p24:.1%}   {p25:.1%}")

# ─── METRIC 6: AI COMPLEXITY RATING (2024-2025) ───────────────────────────────
print("\n[7] Computing complexity ratings (2024-2025)...")

complex_map = {
    "Very well at handling complex tasks": 5,
    "Good, but not great at handling complex tasks": 4,
    "Neither good or bad at handling complex tasks": 3,
    "I don't use AI tools for complex tasks / I don't know": 2,
    "Bad at handling complex tasks": 1,
    "Very poor at handling complex tasks": 0
}

c24_mean = df24['AIComplex'].map(complex_map).mean()
c25_mean = df25['AIComplex'].map(complex_map).mean()
print(f"    2024 mean complexity rating: {c24_mean:.3f}/5")
print(f"    2025 mean complexity rating: {c25_mean:.3f}/5")

# ─── FIG 1: THE BIG PICTURE — 3 METRICS OVER TIME ────────────────────────────
print("\n[8] Generating Figure 1: Big Picture Trends...")

fig = plt.figure(figsize=(18, 10))
fig.patch.set_facecolor('#fafafa')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)
fig.suptitle("AI in Developer Work: 2023 → 2024 → 2025\nStack Overflow Developer Survey Longitudinal Analysis",
             fontsize=15, fontweight='bold', y=0.98)

yrs_label = ['2023','2024','2025']
yrs_x = [0, 1, 2]

# ── 1a. Adoption Rate
ax = fig.add_subplot(gs[0, 0])
adoption = [a23['currently_using'], a24['currently_using'], a25['currently_using']]
ax.plot(yrs_x, [v*100 for v in adoption], 'o-', color=PALETTE[0],
        linewidth=2.5, markersize=9, zorder=3)
for x, v in zip(yrs_x, adoption):
    ax.annotate(f'{v:.1%}', (x, v*100), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=11, fontweight='bold',
                color=PALETTE[0])
ax.fill_between(yrs_x, [v*100 for v in adoption], alpha=0.1, color=PALETTE[0])
ax.set_xticks(yrs_x); ax.set_xticklabels(yrs_label)
ax.set_ylabel('% Currently Using AI'); ax.set_ylim(30, 100)
ax.set_title('AI Adoption Rate', fontweight='bold')
ax.annotate('Question\nwording\nchanged', xy=(2, a25['currently_using']*100),
            xytext=(1.5, 65), fontsize=7.5, color='grey', style='italic',
            arrowprops=dict(arrowstyle='->', color='grey', lw=0.8))

# ── 1b. Sentiment — stacked area
ax = fig.add_subplot(gs[0, 1])
pos = [s23['positive']*100, s24['positive']*100, s25['positive']*100]
neu = [s23['neutral']*100,  s24['neutral']*100,  s25['neutral']*100]
neg = [s23['negative']*100, s24['negative']*100, s25['negative']*100]

ax.stackplot(yrs_x, neg, neu, pos,
             labels=['Negative','Neutral','Positive'],
             colors=['#C44E52','#e0c97e','#55A868'], alpha=0.85)
ax.set_xticks(yrs_x); ax.set_xticklabels(yrs_label)
ax.set_ylabel('% of Respondents'); ax.set_ylim(0, 100)
ax.set_title('AI Sentiment Distribution', fontweight='bold')
ax.legend(loc='upper left', fontsize=8)

# Annotate the drop
for x, v in zip(yrs_x, pos):
    ax.text(x, v + neg[yrs_x.index(x)] + neu[yrs_x.index(x)] + 2,
            f'{v:.0f}%', ha='center', fontsize=9, color='#1a6b3a', fontweight='bold')

# ── 1c. Trust — line chart
ax = fig.add_subplot(gs[0, 2])
high_t = [t23['high']*100, t24['high']*100, t25['high']*100]
low_t  = [t23['low']*100,  t24['low']*100,  t25['low']*100]
ax.plot(yrs_x, high_t, 'o-', color='#55A868', linewidth=2.5, markersize=9, label='Trust (High)')
ax.plot(yrs_x, low_t,  's--', color='#C44E52', linewidth=2.5, markersize=9, label='Distrust (High)')
for x, h, l in zip(yrs_x, high_t, low_t):
    ax.annotate(f'{h:.0f}%', (x, h), textcoords='offset points', xytext=(5, 4),
                fontsize=9, color='#55A868', fontweight='bold')
    ax.annotate(f'{l:.0f}%', (x, l), textcoords='offset points', xytext=(5, -10),
                fontsize=9, color='#C44E52', fontweight='bold')
ax.fill_between(yrs_x, high_t, low_t, alpha=0.08, color='grey')
ax.set_xticks(yrs_x); ax.set_xticklabels(yrs_label)
ax.set_ylabel('%'); ax.set_ylim(0, 75)
ax.set_title('Trust vs. Distrust Over Time', fontweight='bold')
ax.legend(fontsize=8)
ax.annotate('Trust–Distrust\ngap closing', xy=(2, (high_t[2]+low_t[2])/2),
            xytext=(1.2, 55), fontsize=8, color='grey', style='italic',
            arrowprops=dict(arrowstyle='->', color='grey', lw=0.8))

# ── 1d. Threat perception (2024-2025 bar)
ax = fig.add_subplot(gs[1, 0])
threat_yrs = ['2024', '2025']
threat_yes = [th24['yes']*100, th25['yes']*100]
threat_no  = [th24['no']*100,  th25['no']*100]
threat_uns = [th24['unsure']*100, th25['unsure']*100]
x = np.arange(2)
w = 0.25
ax.bar(x - w, threat_no,  w, label='No Threat', color='#55A868', alpha=0.85)
ax.bar(x,     threat_uns, w, label='Unsure',    color='#e0c97e', alpha=0.85)
ax.bar(x + w, threat_yes, w, label='Threatened', color='#C44E52', alpha=0.85)
for i, (n, u, y) in enumerate(zip(threat_no, threat_uns, threat_yes)):
    ax.text(i-w, n+0.5, f'{n:.0f}%', ha='center', fontsize=8)
    ax.text(i,   u+0.5, f'{u:.0f}%', ha='center', fontsize=8)
    ax.text(i+w, y+0.5, f'{y:.0f}%', ha='center', fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(threat_yrs)
ax.set_ylabel('%'); ax.set_title('"Does AI threaten your job?"\n(2024–2025 only)', fontweight='bold')
ax.legend(fontsize=8)

# ── 1e. Task adoption — grouped bars 2023→2025
ax = fig.add_subplot(gs[1, 1:])
show_tasks = ['Writing Code','Debugging/Fixing Code','Documenting Code',
              'Testing Code','Search for Answers','Generating Content','Project Planning']
x = np.arange(len(show_tasks))
w = 0.25
bars23 = [t23_tasks.get(t,0)*100 for t in show_tasks]
bars24 = [t24_tasks.get(t,0)*100 for t in show_tasks]
bars25 = [t25_tasks.get(t,0)*100 for t in show_tasks]

ax.bar(x - w, bars23, w, label='2023', color=list(YEAR_COLORS.values())[0], alpha=0.85)
ax.bar(x,     bars24, w, label='2024', color=list(YEAR_COLORS.values())[1], alpha=0.85)
ax.bar(x + w, bars25, w, label='2025', color=list(YEAR_COLORS.values())[2], alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels([t.replace(' ','\n') for t in show_tasks], fontsize=8)
ax.set_ylabel('% of AISelect Respondents (answered AI usage question)')
ax.set_title('AI Task Usage: Which Tasks Are Developers Using AI For?', fontweight='bold')
ax.legend(fontsize=9)
ax.annotate('Note: 2025 combines "partially AI" + "mostly AI" columns;\n2023/2024 use single "currently using" column',
            xy=(0.01, 0.02), xycoords='axes fraction', fontsize=7, color='grey', style='italic')

plt.savefig('longitudinal_overview.png', bbox_inches='tight', facecolor='#fafafa')
plt.close()
print("    Saved: longitudinal_overview.png")

# ─── FIG 2: THE TRUST–SENTIMENT DIVERGENCE ────────────────────────────────────
print("\n[9] Generating Figure 2: Trust–Sentiment Divergence detail...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("The Growing Confidence Gap: More Adoption, Less Trust\n2023 → 2024 → 2025",
             fontsize=14, fontweight='bold')

# Left: full sentiment breakdown with individual categories
ax = axes[0]
cats = ['Very favorable','Favorable','Indifferent','Unsure','Unfavorable','Very unfavorable']
cat_colors_sent = ['#1a6b3a','#55A868','#e0c97e','#c8b400','#DD8452','#C44E52']

data_by_year = {}
for yr, df, col in [('2023',df23,'AISent'),('2024',df24,'AISent'),('2025',df25,'AISent')]:
    vc = df[col].value_counts()
    total = vc.sum()
    data_by_year[yr] = {c: vc.get(c,0)/total*100 for c in cats}

x = np.arange(len(YEARS))
bottoms = np.zeros(3)
for cat, color in zip(cats, cat_colors_sent):
    vals = [data_by_year[str(y)][cat] for y in YEARS]
    bars = ax.bar(x, vals, bottom=bottoms, color=color, label=cat, alpha=0.88, width=0.5)
    for xi, (v, b) in enumerate(zip(vals, bottoms)):
        if v > 4:
            ax.text(xi, b + v/2, f'{v:.0f}%', ha='center', va='center',
                    fontsize=8.5, color='white', fontweight='bold')
    bottoms += np.array(vals)

ax.set_xticks(x); ax.set_xticklabels([str(y) for y in YEARS])
ax.set_ylabel('% of Respondents')
ax.set_title('Full Sentiment Breakdown by Year')
ax.legend(loc='upper right', fontsize=7, ncol=2)

# Right: trust full breakdown
ax = axes[1]
trust_cats = ['Highly trust','Somewhat trust','Neither trust nor distrust',
              'Somewhat distrust','Highly distrust']
trust_colors = ['#1a6b3a','#55A868','#e0c97e','#DD8452','#C44E52']

trust_data = {}
for yr, df, col in [('2023',df23,'AIBen'),('2024',df24,'AIAcc'),('2025',df25,'AIAcc')]:
    vc = df[col].value_counts()
    valid = {c: vc.get(c,0) for c in trust_cats}
    total = sum(valid.values())
    trust_data[yr] = {c: v/total*100 for c, v in valid.items()} if total > 0 else {c: 0 for c in trust_cats}

bottoms = np.zeros(3)
for cat, color in zip(trust_cats, trust_colors):
    vals = [trust_data[str(y)][cat] for y in YEARS]
    bars = ax.bar(x, vals, bottom=bottoms, color=color, label=cat, alpha=0.88, width=0.5)
    for xi, (v, b) in enumerate(zip(vals, bottoms)):
        if v > 4:
            ax.text(xi, b + v/2, f'{v:.0f}%', ha='center', va='center',
                    fontsize=8.5, color='white', fontweight='bold')
    bottoms += np.array(vals)

ax.set_xticks(x); ax.set_xticklabels([str(y) for y in YEARS])
ax.set_ylabel('% of Respondents (among those answering trust Q)')
ax.set_title('Full Trust Breakdown by Year\n(2023=AIBen col, 2024-25=AIAcc col — same Likert scale)')
ax.legend(loc='upper right', fontsize=7, ncol=2)

# Annotation on trust chart
ax.annotate('"Highly distrust" doubled\n2024→2025',
            xy=(2, trust_data['2025']['Highly distrust'] + trust_data['2025']['Somewhat distrust']),
            xytext=(1.4, 88), fontsize=8, color='#C44E52', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#C44E52', lw=1.2))

plt.tight_layout()
plt.savefig('longitudinal_trust_sentiment.png', bbox_inches='tight')
plt.close()
print("    Saved: longitudinal_trust_sentiment.png")

# ─── FIG 3: THE ADOPTION PARADOX ─────────────────────────────────────────────
print("\n[10] Generating Figure 3: Adoption Paradox...")

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#fafafa')

# Dual axis: adoption vs sentiment vs distrust
ax2 = ax.twinx()

adoption_vals = [a23['currently_using']*100, a24['currently_using']*100, a25['currently_using']*100]
pos_sent_vals = [s23['positive']*100, s24['positive']*100, s25['positive']*100]
high_dist_vals = [t23['highly_distrust']*100, t24['highly_distrust']*100, t25['highly_distrust']*100]

l1 = ax.plot(yrs_x, adoption_vals, 'o-', color='#4C72B0', linewidth=3,
             markersize=12, label='AI Adoption Rate', zorder=3)
l2 = ax.plot(yrs_x, pos_sent_vals, 's--', color='#55A868', linewidth=3,
             markersize=12, label='Positive Sentiment', zorder=3)
l3 = ax2.plot(yrs_x, high_dist_vals, '^:', color='#C44E52', linewidth=3,
              markersize=12, label='"Highly Distrust" Rate', zorder=3)

# Shaded region between adoption and sentiment
ax.fill_between(yrs_x, adoption_vals, pos_sent_vals, alpha=0.1, color='grey',
                label='Adoption–Sentiment gap')

# Annotations
for x, a, s, d in zip(yrs_x, adoption_vals, pos_sent_vals, high_dist_vals):
    ax.annotate(f'{a:.0f}%', (x, a), xytext=(0, 12), textcoords='offset points',
                ha='center', fontsize=11, fontweight='bold', color='#4C72B0')
    ax.annotate(f'{s:.0f}%', (x, s), xytext=(0, -18), textcoords='offset points',
                ha='center', fontsize=11, fontweight='bold', color='#55A868')
    ax2.annotate(f'{d:.1f}%', (x, d), xytext=(8, 0), textcoords='offset points',
                 ha='left', fontsize=10, fontweight='bold', color='#C44E52')

ax.set_xticks(yrs_x)
ax.set_xticklabels(['2023','2024','2025'], fontsize=13)
ax.set_ylabel('% of Survey Respondents', fontsize=11)
ax2.set_ylabel('% Highly Distrusting AI', fontsize=11, color='#C44E52')
ax2.tick_params(axis='y', labelcolor='#C44E52')
ax.set_ylim(30, 105)
ax2.set_ylim(0, 30)
ax.set_title('The AI Adoption Paradox:\nUsage Is Up, Trust & Sentiment Are Down',
             fontsize=14, fontweight='bold', pad=15)

# Combined legend
lines = l1 + l2 + l3 + [mpatches.Patch(alpha=0.1, color='grey', label='Adoption–Sentiment gap')]
labels = [l.get_label() for l in l1+l2+l3] + ['Adoption–Sentiment gap']
ax.legend(lines, labels, loc='lower left', fontsize=10, framealpha=0.9)

# Annotation box
ax.text(1.5, 40,
        '"More developers are using AI than ever before,\nbut trust and enthusiasm are both declining."\n\nAdoption +34pp vs. Sentiment −16pp (2023→2025)',
        fontsize=9, style='italic', color='#333333',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff9e6', edgecolor='#ccaa00', alpha=0.9))

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('longitudinal_paradox.png', bbox_inches='tight', facecolor='#fafafa')
plt.close()
print("    Saved: longitudinal_paradox.png")

# ─── SUMMARY TABLE ────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  LONGITUDINAL SUMMARY")
print("=" * 70)

summary = pd.DataFrame({
    'Metric': [
        'Survey N',
        'AI Adoption (currently using)',
        'Positive Sentiment',
        'Negative Sentiment',
        '"Highly Distrust" AI',
        'Trust (high)',
        'Distrust (high)',
        'Job Threat: Yes',
        'AI Complexity Mean (0-5)',
    ],
    '2023': [
        f"{len(df23):,}",
        f"{a23['currently_using']:.1%}",
        f"{s23['positive']:.1%}",
        f"{s23['negative']:.1%}",
        f"{t23['highly_distrust']:.1%}",
        f"{t23['high']:.1%}",
        f"{t23['low']:.1%}",
        'N/A',
        'N/A',
    ],
    '2024': [
        f"{len(df24):,}",
        f"{a24['currently_using']:.1%}",
        f"{s24['positive']:.1%}",
        f"{s24['negative']:.1%}",
        f"{t24['highly_distrust']:.1%}",
        f"{t24['high']:.1%}",
        f"{t24['low']:.1%}",
        f"{th24['yes']:.1%}",
        f"{c24_mean:.2f}",
    ],
    '2025': [
        f"{len(df25):,}",
        f"{a25['currently_using']:.1%}",
        f"{s25['positive']:.1%}",
        f"{s25['negative']:.1%}",
        f"{t25['highly_distrust']:.1%}",
        f"{t25['high']:.1%}",
        f"{t25['low']:.1%}",
        f"{th25['yes']:.1%}",
        f"{c25_mean:.2f}",
    ],
    'Change 23→25': [
        '−', '+34pp', '−16pp', '+19pp', '+13pp', '−9pp', '+23pp', 'N/A', 'N/A'
    ]
})

print(summary.to_string(index=False))
print("\n  OUTPUTS:")
for f in ['longitudinal_overview.png','longitudinal_trust_sentiment.png','longitudinal_paradox.png']:
    print(f"    {f}")
