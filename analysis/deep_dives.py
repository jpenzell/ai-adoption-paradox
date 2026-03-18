"""
Human–AI Work Patterns: Deep Dive Charts
7 Additional Analyses Beyond the Core Pipeline
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from config import CSV_2023, CSV_2024, CSV_2025, check_data
check_data()

sns.set_theme(style="whitegrid")
PALETTE  = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B2","#937860","#DA8BC3","#8C8C8C"]
DIVERGE  = ["#C44E52","#DD8452","#e0c97e","#55A868","#1a6b3a"]
plt.rcParams['figure.dpi'] = 130

print("=" * 70)
print("  DEEP DIVE ANALYSES — 7 additional findings")
print("=" * 70)

# ─── LOAD ─────────────────────────────────────────────────────────────────────
df25 = pd.read_csv(CSV_2025, low_memory=False)
df24 = pd.read_csv(CSV_2024, low_memory=False)
df23 = pd.read_csv(CSV_2023, low_memory=False)

# Shared encodings
usage_map = {
    "Yes, I use AI tools daily": 4,
    "Yes, I use AI tools weekly": 3,
    "Yes, I use AI tools monthly or infrequently": 2,
    "No, but I plan to soon": 1,
    "No, and I don't plan to": 0
}
trust_map = {
    "Highly trust": 4, "Somewhat trust": 3,
    "Neither trust nor distrust": 2,
    "Somewhat distrust": 1, "Highly distrust": 0
}
complex_map = {
    "Very well at handling complex tasks": 5,
    "Good, but not great at handling complex tasks": 4,
    "Neither good or bad at handling complex tasks": 3,
    "I don't use AI tools for complex tasks / I don't know": 2,
    "Bad at handling complex tasks": 1,
    "Very poor at handling complex tasks": 0
}
sent_map = {
    "Very favorable": 5, "Favorable": 4, "Indifferent": 3,
    "Unsure": 2, "Unfavorable": 1, "Very unfavorable": 0
}

df25['UsageScore']   = df25['AISelect'].map(usage_map)
df25['TrustScore']   = df25['AIAcc'].map(trust_map)
df25['ComplexScore'] = df25['AIComplex'].map(complex_map)
df25['SentScore']    = df25['AISent'].map(sent_map)
df25['WorkExpNum']   = pd.to_numeric(df25['WorkExp'], errors='coerce')
df25['YearsCodeNum'] = pd.to_numeric(df25['YearsCode'], errors='coerce')

# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — THE JOB THREAT PARADOX
# ══════════════════════════════════════════════════════════════════════════════
print("\n[1] Job Threat Paradox...")

fig, axes = plt.subplots(1, 3, figsize=(17, 6))
fig.suptitle("Finding 1: The Job Threat Paradox\n"
             "Developers who feel AI threatens their job use it MORE, not less",
             fontsize=13, fontweight='bold')

threat_order = ["Yes", "I'm not sure", "No"]
threat_labels = ["Feels\nThreatened", "Unsure", "Doesn't Feel\nThreatened"]
threat_colors = ["#C44E52", "#e0c97e", "#55A868"]

# 1a. Mean usage by threat perception
ax = axes[0]
grp = df25[df25['AIThreat'].notna() & df25['UsageScore'].notna()].groupby('AIThreat')
means = [grp.get_group(t)['UsageScore'].mean() for t in threat_order]
ns    = [len(grp.get_group(t)) for t in threat_order]
bars = ax.bar(threat_labels, means, color=threat_colors, width=0.5, edgecolor='white', linewidth=1.5)
ax.set_ylabel('Mean AI Usage Score (0=Never, 4=Daily)')
ax.set_title('AI Usage by Job Threat Perception')
ax.set_ylim(0, 4)
for bar, m, n in zip(bars, means, ns):
    ax.text(bar.get_x()+bar.get_width()/2, m+0.05, f'{m:.2f}\n(n={n:,})',
            ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.axhline(df25['UsageScore'].mean(), color='grey', linestyle='--', alpha=0.6, linewidth=1.5)
ax.text(2.4, df25['UsageScore'].mean()+0.05, 'Overall\nmean', color='grey', fontsize=8)

# 1b. Full usage distribution per threat group
ax = axes[1]
usage_cats = ["Yes, I use AI tools daily","Yes, I use AI tools weekly",
              "Yes, I use AI tools monthly or infrequently",
              "No, but I plan to soon","No, and I don't plan to"]
usage_short = ["Daily","Weekly","Monthly","Plan to","Won't"]
usage_colors = ["#1a6b3a","#55A868","#e0c97e","#DD8452","#C44E52"]

x = np.arange(len(threat_labels))
bottom = np.zeros(3)
for cat, short, color in zip(usage_cats, usage_short, usage_colors):
    vals = []
    for t in threat_order:
        sub = df25[df25['AIThreat'] == t]
        tot = sub['AISelect'].notna().sum()
        vals.append(sub[sub['AISelect'] == cat].shape[0] / tot * 100 if tot > 0 else 0)
    ax.bar(x, vals, bottom=bottom, label=short, color=color, alpha=0.88, width=0.5)
    for xi, (v, b) in enumerate(zip(vals, bottom)):
        if v > 6:
            ax.text(xi, b + v/2, f'{v:.0f}%', ha='center', va='center',
                    fontsize=8, color='white', fontweight='bold')
    bottom += np.array(vals)

ax.set_xticks(x); ax.set_xticklabels(threat_labels)
ax.set_ylabel('% of Group'); ax.set_title('Usage Frequency Distribution\nby Threat Perception')
ax.legend(fontsize=8, loc='lower right')

# 1c. Trust score by threat group
ax = axes[2]
trust_means = [grp.get_group(t)['TrustScore'].dropna().mean() for t in threat_order]
bars = ax.bar(threat_labels, trust_means, color=threat_colors, width=0.5, edgecolor='white', linewidth=1.5)
ax.set_ylabel('Mean Trust Score (0=Highly Distrust, 4=Highly Trust)')
ax.set_title('AI Trust by Job Threat Perception')
ax.set_ylim(0, 3)
for bar, m in zip(bars, trust_means):
    ax.text(bar.get_x()+bar.get_width()/2, m+0.04, f'{m:.2f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.text(0.5, 0.15,
        '"Threatened developers use AI more\nand show higher trust scores —\nanxious early adopters, not avoiders."',
        transform=ax.transAxes, fontsize=9, style='italic',
        bbox=dict(boxstyle='round', facecolor='#fff9e6', edgecolor='#ccaa00', alpha=0.9))

plt.tight_layout()
plt.savefig('deep1_threat_paradox.png', bbox_inches='tight')
plt.close()
print("    Saved: deep1_threat_paradox.png")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 — THE OCCASIONAL USER DIP
# ══════════════════════════════════════════════════════════════════════════════
print("\n[2] The Occasional User Dip...")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Finding 2: The Occasional-User Dip\n"
             "Infrequent users rate AI most harshly — worse than non-users who are planning to try",
             fontsize=13, fontweight='bold')

usage_order = ["No, and I don't plan to", "No, but I plan to soon",
               "Yes, I use AI tools monthly or infrequently",
               "Yes, I use AI tools weekly", "Yes, I use AI tools daily"]
usage_xlabels = ["Won't Use\n(Opt-Out)", "Planning\nto Try",
                 "Monthly/\nOccasional", "Weekly", "Daily"]
ucolors = ["#C44E52","#DD8452","#e0c97e","#55A868","#1a6b3a"]

# 2a. Complexity score by usage frequency
ax = axes[0]
grp_u = df25[df25['AISelect'].notna() & df25['ComplexScore'].notna()].groupby('AISelect')
# Separate group for trust analysis — must filter on TrustScore, not ComplexScore
grp_u_trust = df25[df25['AISelect'].notna() & df25['TrustScore'].notna()].groupby('AISelect')
complex_means = []
complex_cis   = []
ns = []
for cat in usage_order:
    if cat in grp_u.groups:
        vals = grp_u.get_group(cat)['ComplexScore']
        complex_means.append(vals.mean())
        complex_cis.append(1.96 * vals.std() / np.sqrt(len(vals)))
        ns.append(len(vals))
    else:
        complex_means.append(0); complex_cis.append(0); ns.append(0)

bars = ax.bar(range(5), complex_means, color=ucolors, width=0.55,
              edgecolor='white', linewidth=1.5, yerr=complex_cis,
              error_kw={'capsize': 4, 'color': 'black', 'linewidth': 1.5})
ax.set_xticks(range(5)); ax.set_xticklabels(usage_xlabels, fontsize=9)
ax.set_ylabel('Mean AI Complexity Rating (0=Very Poor, 5=Very Well)')
ax.set_title('How Well Does AI Handle Complex Tasks?\nRated by Usage Frequency')
ax.set_ylim(0, 3.5)

# Arrow showing the dip
ax.annotate('', xy=(2, complex_means[2]), xytext=(1, complex_means[1]),
            arrowprops=dict(arrowstyle='->', color='#C44E52', lw=2))
ax.text(1.5, complex_means[2] - 0.25, 'THE DIP', color='#C44E52',
        fontsize=9, fontweight='bold', ha='center')

for i, (m, n) in enumerate(zip(complex_means, ns)):
    ax.text(i, m + 0.12 + complex_cis[i], f'{m:.2f}\nn={n:,}',
            ha='center', fontsize=8)

# 2b. Trust score by usage frequency (use trust-eligible subset, not complexity subset)
ax = axes[1]
trust_means_u = []
for cat in usage_order:
    if cat in grp_u_trust.groups:
        vals = grp_u_trust.get_group(cat)['TrustScore']
        trust_means_u.append(vals.mean())
    else:
        trust_means_u.append(0)

bars = ax.bar(range(5), trust_means_u, color=ucolors, width=0.55, edgecolor='white', linewidth=1.5)
ax.set_xticks(range(5)); ax.set_xticklabels(usage_xlabels, fontsize=9)
ax.set_ylabel('Mean AI Trust Score (0=Highly Distrust, 4=Highly Trust)')
ax.set_title('AI Trust Score by Usage Frequency\n"The more you use it, the more you trust it"')
ax.set_ylim(0, 2.5)
for i, m in enumerate(trust_means_u):
    ax.text(i, m + 0.05, f'{m:.2f}', ha='center', fontsize=9, fontweight='bold')

ax.text(0.5, 0.1,
        '"Occasional use is the danger zone:\nenough exposure to hit limits,\nnot enough to develop competence."',
        transform=ax.transAxes, fontsize=9, style='italic',
        bbox=dict(boxstyle='round', facecolor='#fff9e6', edgecolor='#ccaa00', alpha=0.9))

plt.tight_layout()
plt.savefig('deep2_occasional_dip.png', bbox_inches='tight')
plt.close()
print("    Saved: deep2_occasional_dip.png")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 — HOW YOU LEARNED AI IS ASSOCIATED WITH TRUST
# ══════════════════════════════════════════════════════════════════════════════
print("\n[3] Learning Method → Trust...")

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Finding 3: How You Learned AI Is Associated With How Much You Trust It\n"
             "Structured learning → higher trust; informal/colleague-led → lower trust",
             fontsize=13, fontweight='bold')

# Build learning × trust data
df_learn = df25[df25['AILearnHow'].notna() & df25['AIAcc'].notna()].copy()
learn_exp = df_learn.assign(Method=df_learn['AILearnHow'].str.split(';')).explode('Method')
learn_exp['Method'] = learn_exp['Method'].str.strip()
learn_exp['TrustHigh'] = learn_exp['AIAcc'].isin(['Highly trust','Somewhat trust'])
learn_exp['TrustLow']  = learn_exp['AIAcc'].isin(['Highly distrust','Somewhat distrust'])
learn_exp['UsageHigh'] = learn_exp['UsageScore'] >= 3

lt = learn_exp.groupby('Method').agg(
    TrustRate=('TrustHigh','mean'),
    DistrustRate=('TrustLow','mean'),
    HighUsage=('UsageHigh','mean'),
    N=('TrustHigh','count')
).reset_index()
lt = lt[lt['N'] >= 200].sort_values('TrustRate', ascending=True)

METHOD_LABELS = {
    'AI CodeGen tools or AI-enabled apps': 'AI Tools (self-taught)',
    'Other online resources (e.g. standard search, forum, online community)': 'Online Search/Forums',
    'Technical documentation (is generated for/by the tool or system)': 'Tech Docs',
    'Videos (not associated with specific online course or certification)': 'YouTube/Videos',
    'Blogs or podcasts': 'Blogs/Podcasts',
    'Colleague or on-the-job training': 'Colleague/On-the-Job',
    'Stack Overflow or Stack Exchange': 'Stack Overflow',
    'Online Courses or Certification (includes all media types)': 'Online Courses',
    'Books / Physical media': 'Books',
    'School (i.e., University, College, etc)': 'School/University',
    'Games or coding challenges': 'Games/Challenges',
    'Coding Bootcamp': 'Coding Bootcamp',
    'Other (please specify):': 'Other'
}
lt['ShortMethod'] = lt['Method'].map(METHOD_LABELS).fillna(lt['Method'])
lt = lt.sort_values('TrustRate', ascending=True)

# 3a. Trust rate by method (horizontal bar)
ax = axes[0]
colors = ['#55A868' if v >= 0.44 else '#e0c97e' if v >= 0.38 else '#C44E52'
          for v in lt['TrustRate']]
bars = ax.barh(range(len(lt)), lt['TrustRate']*100, color=colors, height=0.65)
ax.set_yticks(range(len(lt)))
ax.set_yticklabels(lt['ShortMethod'], fontsize=9)
ax.set_xlabel('% Who "Somewhat" or "Highly" Trust AI Output')
ax.set_title('Trust Rate by Learning Method')
for i, (bar, v, n) in enumerate(zip(bars, lt['TrustRate'], lt['N'])):
    ax.text(v*100 + 0.5, i, f'{v:.1%}  (n={n:,})', va='center', fontsize=8)
ax.set_xlim(0, 80)
ax.axvline(lt['TrustRate'].mean()*100, color='grey', linestyle='--', alpha=0.6)
ax.text(lt['TrustRate'].mean()*100 + 0.3, -0.7, 'Avg', fontsize=8, color='grey')

# Add category bands
for label, y_range, color in [
    ('Structured\nLearning', (8.5, 11.5), '#e8f5e9'),
    ('Self-Directed\nDigital', (3.5, 8.5), '#fff8e1'),
    ('Informal/\nSocial', (-0.5, 3.5), '#ffebee')
]:
    ax.axhspan(y_range[0], y_range[1], alpha=0.15, color=color, zorder=0)
    ax.text(-2, (y_range[0]+y_range[1])/2, label, va='center', ha='right',
            fontsize=7.5, color='grey', style='italic')

# 3b. Scatter: trust rate vs daily usage rate by method
ax = axes[1]
scatter = ax.scatter(lt['TrustRate']*100, lt['HighUsage']*100,
                     s=lt['N']/20, c=lt['TrustRate'],
                     cmap='RdYlGn', alpha=0.85, edgecolors='grey', linewidth=0.5,
                     vmin=0.3, vmax=0.7)
for _, row in lt.iterrows():
    ax.annotate(row['ShortMethod'], (row['TrustRate']*100, row['HighUsage']*100),
                fontsize=7.5, xytext=(4, 3), textcoords='offset points', alpha=0.9)
plt.colorbar(scatter, ax=ax, label='Trust Rate')
ax.set_xlabel('Trust Rate (%)')
ax.set_ylabel('High Usage Rate (weekly or daily, %)')
ax.set_title('Learning Method: Trust vs. Usage\n(bubble size = number of respondents)')
ax.axhline(lt['HighUsage'].mean()*100, color='grey', linestyle='--', alpha=0.4)
ax.axvline(lt['TrustRate'].mean()*100, color='grey', linestyle='--', alpha=0.4)
ax.text(lt['TrustRate'].mean()*100+0.3, lt['HighUsage'].min()*100, 'Avg trust', fontsize=7.5, color='grey')
ax.text(lt['TrustRate'].min()*100, lt['HighUsage'].mean()*100+0.3, 'Avg usage', fontsize=7.5, color='grey')

plt.tight_layout()
plt.savefig('deep3_learning_trust.png', bbox_inches='tight')
plt.close()
print("    Saved: deep3_learning_trust.png")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 — THE FRUSTRATION–DISTRUST PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
print("\n[4] Frustration → Distrust pipeline...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Finding 4: The Frustration–Distrust Pipeline\n"
             "It's not that AI is wrong — it's that developers can't interrogate or own the output",
             fontsize=13, fontweight='bold')

df_frust = df25[df25['AIFrustration'].notna() & df25['AIAcc'].notna()].copy()
fexp = df_frust.assign(F=df_frust['AIFrustration'].str.split(';')).explode('F')
fexp['F'] = fexp['F'].str.strip()
fexp['IsDistrust'] = fexp['AIAcc'].isin(['Highly distrust','Somewhat distrust'])
fexp['IsHighDist']  = fexp['AIAcc'] == 'Highly distrust'
fexp['IsHighTrust'] = fexp['AIAcc'] == 'Highly trust'

FRUST_SHORT = {
    "AI solutions that are almost right, but not quite": "Almost-right\nbut not quite",
    "Debugging AI-generated code is more time-consuming": "Debugging AI code\nis slower",
    "I don't use AI tools regularly": "Don't use AI\nregularly",
    "I've become less confident in my own problem-solving": "Lost confidence\nin own skills",
    "It's hard to understand how or why the code works": "Can't understand\nAI's reasoning",
    "Other (write in):": "Other",
    "I haven't encountered any problems": "No problems\nencountered"
}

ft = fexp.groupby('F').agg(
    DistrustRate=('IsDistrust','mean'),
    HighDistrustRate=('IsHighDist','mean'),
    N=('IsDistrust','count')
).reset_index()
ft = ft[ft['N'] >= 500].sort_values('DistrustRate', ascending=False)
ft['Short'] = ft['F'].map(FRUST_SHORT).fillna(ft['F'])

# 4a. Distrust rate by frustration type
ax = axes[0]
bar_colors = ['#C44E52' if v > 0.45 else '#DD8452' if v > 0.35 else '#55A868'
              for v in ft['DistrustRate']]
bars = ax.barh(range(len(ft)), ft['DistrustRate']*100, color=bar_colors, height=0.6)
ax.set_yticks(range(len(ft)))
ax.set_yticklabels(ft['Short'], fontsize=9)
ax.set_xlabel('% Who Distrust AI ("Somewhat" or "Highly")')
ax.set_title('Distrust Rate Among Those\nExperiencing Each Frustration')
for i, (bar, v, n) in enumerate(zip(bars, ft['DistrustRate'], ft['N'])):
    ax.text(v*100 + 0.3, i, f'{v:.1%}  n={n:,}', va='center', fontsize=8.5)
ax.set_xlim(0, 100)

# Annotate the key insight
ax.annotate('"Debugging AI code is slower" and\n"Can\'t understand AI\'s reasoning"\npredict distrust more than\n"almost right" frustration',
            xy=(ft[ft['Short']=="Debugging AI code\nis slower"]['DistrustRate'].values[0]*100, 
                ft[ft['Short']=="Debugging AI code\nis slower"].index[0]),
            xytext=(40, 5), fontsize=8, style='italic',
            arrowprops=dict(arrowstyle='->', color='#C44E52', lw=1.2),
            color='#C44E52')

# 4b. Stacked full sentiment breakdown per frustration
ax = axes[1]
sent_cats  = ['Very favorable','Favorable','Indifferent','Unsure','Unfavorable','Very unfavorable']
sent_colors_bar = ['#1a6b3a','#55A868','#e0c97e','#c8b400','#DD8452','#C44E52']
sent_short = ['V.Fav','Fav','Indiff','Unsure','Unfav','V.Unfav']

x = np.arange(len(ft))
bottoms = np.zeros(len(ft))
for cat, color, short in zip(sent_cats, sent_colors_bar, sent_short):
    vals = []
    for f_val in ft['F']:
        sub = fexp[fexp['F'] == f_val]
        tot = sub['AISent'].notna().sum()
        vals.append(sub[sub['AISent']==cat].shape[0]/tot*100 if tot > 0 else 0)
    ax.bar(x, vals, bottom=bottoms, color=color, label=short, alpha=0.88, width=0.55)
    for xi, (v, b) in enumerate(zip(vals, bottoms)):
        if v > 8:
            ax.text(xi, b+v/2, f'{v:.0f}%', ha='center', va='center',
                    fontsize=7.5, color='white', fontweight='bold')
    bottoms += np.array(vals)

ax.set_xticks(x)
ax.set_xticklabels(ft['Short'], fontsize=8, rotation=20, ha='right')
ax.set_ylabel('% Sentiment Response')
ax.set_title('Full Sentiment Breakdown\nby Frustration Type')
ax.legend(fontsize=7.5, ncol=3, loc='upper right')

plt.tight_layout()
plt.savefig('deep4_frustration_pipeline.png', bbox_inches='tight')
plt.close()
print("    Saved: deep4_frustration_pipeline.png")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 5 — EXPERIENCE CURVE (non-linear trust/usage)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[5] Experience curve...")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Finding 5: The Earned Skepticism Curve\n"
             "Trust and usage both decline consistently with experience — veterans are the hardest to convert",
             fontsize=13, fontweight='bold')

bins   = [0, 2, 5, 10, 15, 20, 35]
labels = ['0–2\n(Junior)', '3–5\n(Early-Mid)', '6–10\n(Mid)', '11–15\n(Senior)', '16–20\n(Late-Senior)', '20+\n(Veteran)']
df25['ExpBin'] = pd.cut(df25['WorkExpNum'], bins=bins, labels=labels)

exp_grp = df25[df25['ExpBin'].notna()].groupby('ExpBin', observed=True)
exp_trust   = exp_grp['TrustScore'].agg(['mean','sem','count'])
exp_usage   = exp_grp['UsageScore'].agg(['mean','sem','count'])
exp_complex = exp_grp['ComplexScore'].agg(['mean','sem'])
exp_sent    = exp_grp['SentScore'].agg(['mean','sem'])

x = np.arange(len(labels))

# 5a. Trust and Usage by Experience
ax = axes[0]
ax2 = ax.twinx()
l1 = ax.errorbar(x, exp_trust['mean'], yerr=exp_trust['sem']*1.96,
                 fmt='o-', color='#55A868', linewidth=2.5, markersize=9,
                 capsize=4, label='Trust Score (left)')
l2 = ax2.errorbar(x, exp_usage['mean'], yerr=exp_usage['sem']*1.96,
                  fmt='s--', color='#4C72B0', linewidth=2.5, markersize=9,
                  capsize=4, label='Usage Score (right)')
ax.fill_between(x, exp_trust['mean']-exp_trust['sem']*1.96,
                exp_trust['mean']+exp_trust['sem']*1.96, alpha=0.1, color='#55A868')
ax2.fill_between(x, exp_usage['mean']-exp_usage['sem']*1.96,
                 exp_usage['mean']+exp_usage['sem']*1.96, alpha=0.1, color='#4C72B0')
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel('Mean Trust Score (0–4)', color='#55A868')
ax2.set_ylabel('Mean Usage Score (0–4)', color='#4C72B0')
ax.set_title('Trust & Usage by Years of Experience')
lines = [l1, l2]
labs  = [l.get_label() for l in lines]
ax.legend(lines, labs, loc='upper right', fontsize=8)
# Annotate n per bin
for xi, (idx, row) in enumerate(exp_trust.iterrows()):
    ax.text(xi, 0.05, f'n={row["count"]:,}', ha='center', fontsize=7, color='grey')

# 5b. All 4 metrics normalized across experience bins
ax = axes[1]
metrics = {
    'Trust': exp_trust['mean'],
    'Usage': exp_usage['mean'],
    'Complexity\nRating': exp_complex['mean'],
    'Sentiment': exp_sent['mean']
}
colors_m = ['#55A868','#4C72B0','#8172B2','#DD8452']
for (metric, vals), color in zip(metrics.items(), colors_m):
    normed = (vals - vals.min()) / (vals.max() - vals.min())
    ax.plot(x, normed, 'o-', label=metric, color=color, linewidth=2, markersize=8)

ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel('Normalized Score (0=min, 1=max)')
ax.set_title('All Metrics Normalized by Experience\n(shows direction of change, not absolute values)')
ax.legend(fontsize=9)
ax.text(0.5, 0.05,
        '"Every metric declines with experience.\nVeterans have seen hype cycles before."',
        transform=ax.transAxes, ha='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round', facecolor='#fff9e6', edgecolor='#ccaa00', alpha=0.9))

plt.tight_layout()
plt.savefig('deep5_experience_curve.png', bbox_inches='tight')
plt.close()
print("    Saved: deep5_experience_curve.png")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 6 — STACK OVERFLOW SELF-CANNIBALIZATION
# ══════════════════════════════════════════════════════════════════════════════
print("\n[6] Stack Overflow self-cannibalization...")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Finding 6: Stack Overflow's Most Engaged Users Are Its Most AI-Resistant\n"
             "The platform's power users are the ones most likely to opt out of AI tools",
             fontsize=13, fontweight='bold')

so_order = [
    'Multiple times per day',
    'Daily or almost daily',
    'A few times per week',
    'A few times per month or weekly',
    'Less than once per month or monthly',
    'Less than once every 2 - 3 months',
    'Infrequently, less than once per year',
]
so_labels = [
    'Multiple times/day\n(Power User)',
    'Daily',
    'Few times/week',
    'Few times/month',
    'Monthly',
    'Every 2–3 months',
    'Rarely',
]

df_so = df25[df25['SOVisitFreq'].notna() & df25['AISelect'].notna() & df25['UsageScore'].notna()]

# 6a. % opting out vs mean usage by SO visit freq
ax = axes[0]
results = []
for freq in so_order:
    sub = df_so[df_so['SOVisitFreq'] == freq]
    if len(sub) > 50:
        opt_out = (sub['AISelect'] == "No, and I don't plan to").mean() * 100
        daily   = (sub['AISelect'] == "Yes, I use AI tools daily").mean() * 100
        mean_u  = sub['UsageScore'].mean()
        results.append({'freq': freq, 'opt_out': opt_out, 'daily': daily,
                        'mean_usage': mean_u, 'n': len(sub)})

res_df = pd.DataFrame(results)
x = np.arange(len(res_df))
w = 0.35
b1 = ax.bar(x - w/2, res_df['opt_out'], w, color='#C44E52', alpha=0.85, label='No plans to use AI (%)')
b2 = ax.bar(x + w/2, res_df['daily'],   w, color='#55A868', alpha=0.85, label='Use AI Daily (%)')
ax.set_xticks(x)
ax.set_xticklabels([so_labels[so_order.index(r)] for r in res_df['freq']],
                   fontsize=7.5, rotation=20, ha='right')
ax.set_ylabel('% of Group')
ax.set_title('AI Adoption Behavior by Stack Overflow Visit Frequency')
ax.legend(fontsize=9)
for bar in b1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f'{bar.get_height():.0f}%', ha='center', fontsize=7.5, color='#C44E52')
for bar in b2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f'{bar.get_height():.0f}%', ha='center', fontsize=7.5, color='#1a6b3a')

ax.annotate('Power users:\nhighest opt-out,\nlowest daily AI use',
            xy=(0, res_df['opt_out'].iloc[0]),
            xytext=(1.5, res_df['opt_out'].iloc[0]+5),
            fontsize=8, color='#C44E52', style='italic',
            arrowprops=dict(arrowstyle='->', color='#C44E52'))

# 6b. Mean usage score across SO freq (line)
ax = axes[1]
ax.plot(x, res_df['mean_usage'], 'o-', color='#4C72B0', linewidth=2.5, markersize=10)
ax.fill_between(x, res_df['mean_usage'], alpha=0.15, color='#4C72B0')
ax.set_xticks(x)
ax.set_xticklabels([so_labels[so_order.index(r)] for r in res_df['freq']],
                   fontsize=7.5, rotation=20, ha='right')
ax.set_ylabel('Mean AI Usage Score (0=Never, 4=Daily)')
ax.set_title('Mean AI Usage Score by SO Visit Frequency\n(Most engaged SO users = lowest AI usage)')
for xi, (u, n) in enumerate(zip(res_df['mean_usage'], res_df['n'])):
    ax.text(xi, u+0.04, f'{u:.2f}\n(n={n:,})', ha='center', fontsize=8)
ax.set_ylim(1.5, 3.5)
ax.text(0.5, 0.1,
        '"SO power users rely on human-curated knowledge.\nAI search is a direct threat to that ecosystem."',
        transform=ax.transAxes, ha='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round', facecolor='#fff9e6', edgecolor='#ccaa00', alpha=0.9))

plt.tight_layout()
plt.savefig('deep6_so_cannibalization.png', bbox_inches='tight')
plt.close()
print("    Saved: deep6_so_cannibalization.png")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 7 — AGENT USERS: THE REALISM SHIFT
# ══════════════════════════════════════════════════════════════════════════════
print("\n[7] Agent users — the realism shift...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Finding 7: Agents and the Realism Shift\n"
             "Daily agent users show lower enthusiasm but also far less negativity — they've moved to pragmatism",
             fontsize=13, fontweight='bold')

agent_order = [
    "No, and I don't plan to",
    "No, I use AI exclusively in copilot/autocomplete mode",
    "No, but I plan to",
    "Yes, I use AI agents at work monthly or infrequently",
    "Yes, I use AI agents at work weekly",
    "Yes, I use AI agents at work daily",
]
agent_labels = [
    "Won't Use\nAgents",
    "Copilot\nOnly",
    "Planning\nto Use",
    "Monthly\nAgent Use",
    "Weekly\nAgent Use",
    "Daily\nAgent Use",
]

df_ag = df25[df25['AIAgents'].notna() & df25['AISent'].notna() & df25['TrustScore'].notna()]

# 7a. Full sentiment distribution per agent level
ax = axes[0]
sent_cats_ag = ['Very favorable','Favorable','Indifferent','Unsure','Unfavorable','Very unfavorable']
sc_colors    = ['#1a6b3a','#55A868','#e0c97e','#c8b400','#DD8452','#C44E52']
sc_short     = ['V.Fav','Fav','Indiff','Unsure','Unfav','V.Unfav']

x = np.arange(len(agent_order))
bottoms = np.zeros(len(agent_order))
for cat, color, short in zip(sent_cats_ag, sc_colors, sc_short):
    vals = []
    for ag in agent_order:
        sub = df_ag[df_ag['AIAgents'] == ag]
        tot = sub['AISent'].notna().sum()
        vals.append(sub[sub['AISent']==cat].shape[0]/tot*100 if tot>0 else 0)
    ax.bar(x, vals, bottom=bottoms, color=color, label=short, alpha=0.88, width=0.55)
    for xi, (v, b) in enumerate(zip(vals, bottoms)):
        if v > 8:
            ax.text(xi, b+v/2, f'{v:.0f}%', ha='center', va='center',
                    fontsize=8, color='white', fontweight='bold')
    bottoms += np.array(vals)
ax.set_xticks(x); ax.set_xticklabels(agent_labels, fontsize=8)
ax.set_ylabel('% Sentiment Response')
ax.set_title('Full Sentiment by Agent Engagement Level')
ax.legend(fontsize=7.5, ncol=2, loc='upper left')

# 7b. Mean trust + complexity by agent level (dual axis)
ax = axes[1]
ax2 = ax.twinx()

trust_by_ag   = [df_ag[df_ag['AIAgents']==ag]['TrustScore'].mean()   for ag in agent_order]
complex_by_ag = [df25[df25['AIAgents']==ag]['ComplexScore'].dropna().mean() for ag in agent_order]

l1 = ax.plot(x, trust_by_ag, 'o-', color='#55A868', linewidth=2.5, markersize=10, label='Trust Score')
l2 = ax2.plot(x, complex_by_ag, 's--', color='#8172B2', linewidth=2.5, markersize=10, label='Complexity Rating')
ax.fill_between(x, trust_by_ag, alpha=0.1, color='#55A868')

ax.set_xticks(x); ax.set_xticklabels(agent_labels, fontsize=8)
ax.set_ylabel('Mean Trust (0–4)', color='#55A868')
ax2.set_ylabel('Mean Complexity Rating (0–5)', color='#8172B2')
ax.set_title('Trust & Complexity Rating\nby Agent Engagement Level')
for xi, (t, c) in enumerate(zip(trust_by_ag, complex_by_ag)):
    ax.text(xi, t+0.04, f'{t:.2f}', ha='center', fontsize=8.5, color='#55A868', fontweight='bold')
    ax2.text(xi, c+0.05, f'{c:.2f}', ha='center', fontsize=8.5, color='#8172B2', fontweight='bold')

lines = l1+l2
labs  = [l.get_label() for l in lines]
ax.legend(lines, labs, loc='upper left', fontsize=8)
ax.text(0.5, 0.08,
        '"Daily agent users have the highest trust AND highest\ncomplexity ratings — they\'ve pushed through to mastery."',
        transform=ax.transAxes, ha='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round', facecolor='#fff9e6', edgecolor='#ccaa00', alpha=0.9))

plt.tight_layout()
plt.savefig('deep7_agent_realism.png', bbox_inches='tight')
plt.close()
print("    Saved: deep7_agent_realism.png")

# ══════════════════════════════════════════════════════════════════════════════
# BONUS: WHEN DO DEVELOPERS GO HUMAN? (AIHuman)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[BONUS] When do developers go human...")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Bonus Finding: When Developers Deliberately Choose Humans Over AI\n"
             "Trust gaps, learning goals, and ethical concerns drive the switch — not inability",
             fontsize=13, fontweight='bold')

human_exp = df25[df25['AIHuman'].notna()].assign(
    Reason=df25['AIHuman'].str.split(';')).explode('Reason')
human_exp['Reason'] = human_exp['Reason'].str.strip()

HUMAN_SHORT = {
    "When I don't trust AI's answers": "Don't trust AI's\nanswers",
    "When I have ethical or security concerns about code": "Ethical/security\nconcerns",
    "When I want to fully understand something": "Want to fully\nunderstand",
    "When I want to learn best practices": "Learning best\npractices",
    "When I'm stuck and can't explain the problem": "Stuck / can't\nexplain problem",
    "When I need help fixing complex or unfamiliar code": "Complex/unfamiliar\ncode",
    "When I want to compare different solutions": "Comparing\nsolutions",
    "When I need quick help troubleshooting": "Quick\ntroubleshooting",
    "I don't think I'll need help from people anymore": "Won't need\nhumans anymore",
    "Other (please specify):": "Other"
}
human_exp['Short'] = human_exp['Reason'].map(HUMAN_SHORT).fillna(human_exp['Reason'])

hr = human_exp.groupby('Short').agg(
    N=('Short','count'),
    MeanUsage=('UsageScore','mean'),
    MeanTrust=('TrustScore','mean')
).reset_index()
hr = hr[hr['N'] > 500].sort_values('N', ascending=True)

# Bonus a. Frequency of each "go human" reason
ax = axes[0]
pct = hr['N'] / df25['AIHuman'].notna().sum() * 100
bars = ax.barh(range(len(hr)), pct, color=PALETTE[:len(hr)], height=0.65)
ax.set_yticks(range(len(hr)))
ax.set_yticklabels(hr['Short'], fontsize=9)
ax.set_xlabel('% of Respondents Citing This Reason')
ax.set_title('Why Developers Choose Humans Over AI\n(% of respondents, multi-select)')
for i, (bar, v) in enumerate(zip(bars, pct)):
    ax.text(v+0.2, i, f'{v:.1f}%', va='center', fontsize=8.5)

# Bonus b. Usage score among each "go human" group — do heavy users keep more human tasks?
ax = axes[1]
ax2 = ax.twinx()
l1 = ax.barh(range(len(hr)), hr['MeanUsage'], color='#4C72B0', alpha=0.6, height=0.35,
             label='Mean AI Usage')
l2 = ax2.barh(np.arange(len(hr))+0.35, hr['MeanTrust'], color='#DD8452', alpha=0.6, height=0.35,
              label='Mean AI Trust')
ax.set_yticks(range(len(hr)))
ax.set_yticklabels(hr['Short'], fontsize=9)
ax.set_xlabel('Mean AI Usage Score', color='#4C72B0')
ax2.set_xlabel('Mean AI Trust Score', color='#DD8452')
ax.set_title('AI Usage & Trust Among Each\n"Go Human" Group')
ax.tick_params(axis='x', labelcolor='#4C72B0')
ax2.tick_params(axis='x', labelcolor='#DD8452')
handles = [mpatches.Patch(color='#4C72B0', alpha=0.6, label='Mean AI Usage'),
           mpatches.Patch(color='#DD8452', alpha=0.6, label='Mean AI Trust')]
ax.legend(handles=handles, fontsize=8, loc='lower right')

plt.tight_layout()
plt.savefig('deep_bonus_go_human.png', bbox_inches='tight')
plt.close()
print("    Saved: deep_bonus_go_human.png")

print("\n" + "="*70)
print("  ALL DEEP DIVE CHARTS COMPLETE")
print("="*70)
print("  Files:")
for f in ['deep1_threat_paradox.png','deep2_occasional_dip.png',
          'deep3_learning_trust.png','deep4_frustration_pipeline.png',
          'deep5_experience_curve.png','deep6_so_cannibalization.png',
          'deep7_agent_realism.png','deep_bonus_go_human.png']:
    print(f"    {f}")
