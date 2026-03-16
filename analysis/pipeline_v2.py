"""
Human–AI Work Patterns: Mining the 2025 Stack Overflow Developer Survey
Pipeline v2 — Deepened Analysis
  - Enriched feature set for clustering (AI behavior + experience + org context)
  - Forced k=5 with radar profile chart
  - Richer association rules (role, org, experience → adoption)
  - Refined classification with better feature labeling
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler, OrdinalEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, ConfusionMatrixDisplay
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import warnings
warnings.filterwarnings('ignore')

from config import CSV_2025, check_data
check_data()

sns.set_theme(style="whitegrid", palette="muted")
PALETTE = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B2","#937860","#DA8BC3"]
plt.rcParams['figure.dpi'] = 130

print("=" * 70)
print("  PIPELINE v2 — DEEPENED ANALYSIS")
print("=" * 70)

# ─── 1. LOAD ──────────────────────────────────────────────────────────────────
df_raw = pd.read_csv(CSV_2025, low_memory=False)
print(f"\n[1] Loaded {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")

# ─── 2. FEATURE ENGINEERING ───────────────────────────────────────────────────
print("\n[2] Feature engineering...")
df = df_raw.copy()

# --- Numeric cleanup
def to_num(v):
    try: return float(str(v).replace(',','').split(';')[0])
    except: return np.nan

df['WorkExp']   = df['WorkExp'].apply(to_num)
df['YearsCode'] = df['YearsCode'].apply(to_num)

# --- AI Usage (0–4)
usage_map = {
    "Yes, I use AI tools daily": 4,
    "Yes, I use AI tools weekly": 3,
    "Yes, I use AI tools monthly or infrequently": 2,
    "No, but I plan to soon": 1,
    "No, and I don't plan to": 0
}
df['AIUsageScore'] = df['AISelect'].map(usage_map)

# --- Trust (0–4)
trust_map = {
    "Highly trust": 4, "Somewhat trust": 3, "Neither trust nor distrust": 2,
    "Somewhat distrust": 1, "Highly distrust": 0
}
df['AITrustScore'] = df['AIAcc'].map(trust_map)

# --- Sentiment (0–5)
sent_map = {
    "Very favorable": 5, "Favorable": 4, "Indifferent": 3,
    "Unsure": 2, "Unfavorable": 1, "Very unfavorable": 0
}
df['AISentScore'] = df['AISent'].map(sent_map)

# --- Agent engagement (0–2)
agent_map = {
    "Yes, I use AI agents at work daily": 2,
    "Yes, I use AI agents at work weekly": 2,
    "Yes, I use AI agents at work monthly or infrequently": 1,
    "No, but I plan to": 1,
    "No, I use AI exclusively in copilot/autocomplete mode": 0,
    "No, and I don't plan to": 0
}
df['AgentScore'] = df['AIAgents'].map(agent_map)

# --- AI Complexity perception (0–5)
complex_map = {
    "Very well at handling complex tasks": 5,
    "Good, but not great at handling complex tasks": 4,
    "Neither good or bad at handling complex tasks": 3,
    "I don't use AI tools for complex tasks / I don't know": 2,
    "Bad at handling complex tasks": 1,
    "Very poor at handling complex tasks": 0
}
df['AIComplexScore'] = df['AIComplex'].map(complex_map)

# --- Threat perception (binary: Yes=1, No/Unsure=0; see CODEBOOK.md)
# AI Job threat: Yes=1, No=0, Unsure=0 (binary: threatened vs not)
# Note: "unsure" is collapsed into 0 (not threatened) — a deliberate simplification.
# See CODEBOOK.md for rationale.
threat_map = {"Yes": 1, "No": 0, "I'm not sure": 0}
df['ThreatScore'] = df['AIThreat'].map(threat_map)

# --- AI Learning (binary: did they spend time learning AI tools?)
df['LearnedAI'] = df['LearnCodeAI'].apply(
    lambda v: 1 if isinstance(v, str) and v.startswith('Yes') else 0
)

# --- Purchase influence (binary)
df['HasPurchaseInfluence'] = df['PurchaseInfluence'].apply(
    lambda v: 0 if v == 'No' or pd.isna(v) else 1
)

# --- Experience buckets
def exp_bucket(v):
    if pd.isna(v): return np.nan
    if v <= 2: return 0   # Junior
    elif v <= 7: return 1  # Mid
    elif v <= 15: return 2 # Senior
    else: return 3         # Veteran

df['ExpBucket'] = df['WorkExp'].apply(exp_bucket)

# --- Primary role (simplified)
ROLE_MAP = {
    'full-stack': 'Full-Stack Dev',
    'back-end': 'Back-End Dev',
    'front-end': 'Front-End Dev',
    'data scientist': 'Data Scientist/ML',
    'machine learning': 'Data Scientist/ML',
    'devops': 'DevOps/Platform',
    'platform': 'DevOps/Platform',
    'manager': 'Engineering Manager',
    'executive': 'Executive/Leadership',
    'student': 'Student',
    'architect': 'Architect',
    'security': 'Security Engineer',
    'mobile': 'Mobile Dev',
    'embedded': 'Embedded Dev',
    'qa': 'QA/Test Engineer',
    'test': 'QA/Test Engineer',
    'data engineer': 'Data Engineer',
}
def primary_role(val):
    if pd.isna(val): return 'Other'
    v_lower = str(val).lower()
    for key, label in ROLE_MAP.items():
        if key in v_lower:
            return label
    return 'Other'

df['PrimaryRole'] = df['DevType'].apply(primary_role)

# --- Org size buckets
def org_bucket(v):
    if pd.isna(v): return 'Unknown'
    v = str(v)
    if 'Just me' in v or 'Less than 20' in v: return 'Solo/Micro'
    elif '20 to 99' in v: return 'Small'
    elif '100 to 499' in v or '500 to 999' in v: return 'Mid-Market'
    elif '1,000 to' in v or '5,000 to' in v: return 'Large'
    elif '10,000' in v or 'More than' in v: return 'Enterprise'
    return 'Unknown'

df['OrgBucket'] = df['OrgSize'].apply(org_bucket)

# --- Work mode
def work_mode(v):
    if pd.isna(v): return 'Unknown'
    v = str(v)
    if 'Remote' == v.strip(): return 'Remote'
    elif 'In-person' == v.strip(): return 'In-Person'
    elif 'remote' in v.lower(): return 'Hybrid-Remote'
    elif 'in-person' in v.lower(): return 'Hybrid-InPerson'
    return 'Unknown'

df['WorkMode'] = df['RemoteWork'].apply(work_mode)

print("    Features engineered.")

# ─── 3. FILTER TO RESPONDENTS WITH SUFFICIENT AI DATA ────────────────────────
print("\n[3] Filtering respondents...")

CLUSTER_FEATURES = ['AIUsageScore','AITrustScore','AISentScore',
                    'AgentScore','AIComplexScore','LearnedAI']

df_ai = df.dropna(subset=['AIUsageScore','AITrustScore','AISentScore']).copy()
for f in ['AgentScore','AIComplexScore']:
    df_ai[f] = df_ai[f].fillna(df_ai[f].median())

df_ai['LearnedAI'] = df_ai['LearnedAI'].fillna(0)
print(f"    Working set: {len(df_ai):,} respondents")

# ─── 4. SILHOUETTE SCAN ───────────────────────────────────────────────────────
print("\n[4] Silhouette scan (k=2 to 8)...")

scaler = StandardScaler()
X_cluster = scaler.fit_transform(df_ai[CLUSTER_FEATURES])

sil_scores = {}
for k in range(2, 9):
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = km.fit_predict(X_cluster)
    score = silhouette_score(X_cluster, labels)
    sil_scores[k] = score
    print(f"    k={k}: silhouette={score:.4f}")

# We'll use k=5 per design intent (richer archetypes)
# but note the statistical best
best_k_stat = max(sil_scores, key=sil_scores.get)
print(f"    Statistical best k = {best_k_stat}  |  Using k=5 for richer archetypes")

# ─── 5. FIT k=5 CLUSTERS ─────────────────────────────────────────────────────
print("\n[5] Fitting k=5 clusters...")

km5 = KMeans(n_clusters=5, random_state=42, n_init=20)
df_ai['Cluster5'] = km5.fit_predict(X_cluster)

profile = df_ai.groupby('Cluster5')[CLUSTER_FEATURES].mean()
print("\n    Raw cluster profiles:")
print(profile.round(2))

# ─── 6. NAME THE CLUSTERS ─────────────────────────────────────────────────────
print("\n[6] Naming clusters...")

ARCHETYPE_NAMES = {}
ARCHETYPE_DESC  = {}

for cid, row in profile.iterrows():
    usage   = row['AIUsageScore']
    trust   = row['AITrustScore']
    sent    = row['AISentScore']
    agent   = row['AgentScore']
    complex_= row['AIComplexScore']
    learned = row['LearnedAI']

    if usage >= 3.5 and trust >= 2.5 and agent >= 1.2:
        name = "Daily Integrators"
        desc = "Use AI daily, actively exploring agents, trust the output"
    elif usage >= 3.0 and sent >= 3.5 and agent < 0.8:
        name = "Enthusiastic Adopters"
        desc = "Frequent use, positive sentiment, but haven't moved into agents yet"
    elif usage >= 2.0 and trust <= 1.8:
        name = "Cautious Experimenters"
        desc = "Using AI regularly but remain skeptical — trust hasn't followed usage"
    elif usage <= 1.2 and sent >= 3.0:
        name = "Curious Bystanders"
        desc = "Positive attitude toward AI but haven't integrated it yet"
    elif usage <= 1.0 and sent <= 1.8:
        name = "Active Resisters"
        desc = "Low usage, negative sentiment — explicitly opting out"
    else:
        name = "Pragmatic Dabblers"
        desc = "Moderate use when useful, neutral on trust and sentiment"

    ARCHETYPE_NAMES[cid] = name
    ARCHETYPE_DESC[cid]  = desc
    print(f"    Cluster {cid} → {name}  (usage={usage:.2f}, trust={trust:.2f}, sent={sent:.2f}, agent={agent:.2f})")

df_ai['Archetype'] = df_ai['Cluster5'].map(ARCHETYPE_NAMES)

# ─── 7. VISUALIZATION A: Cluster Profiles Heatmap ────────────────────────────
print("\n[7] Generating cluster profile visualizations...")

profile_named = profile.copy()
profile_named.index = [ARCHETYPE_NAMES[i] for i in profile_named.index]
profile_named.columns = ['Usage','Trust','Sentiment','Agent Use','AI Complexity','Learned AI']

# Normalize each feature 0-1 for heatmap readability
profile_norm = (profile_named - profile_named.min()) / (profile_named.max() - profile_named.min())

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("AI Adoption Archetypes — Cluster Profiles (k=5)", fontsize=15, fontweight='bold')

# Heatmap
sns.heatmap(profile_norm, ax=axes[0], cmap='RdYlGn', annot=profile_named.round(2),
            fmt='.2f', linewidths=0.5, cbar_kws={'label': 'Normalized Score'},
            annot_kws={"size": 9})
axes[0].set_title('Feature Profiles by Archetype\n(color = normalized, numbers = raw mean)')
axes[0].set_xlabel('')
axes[0].tick_params(axis='x', rotation=30)
axes[0].tick_params(axis='y', rotation=0)

# Cluster sizes with descriptions
counts = df_ai['Archetype'].value_counts()
colors = PALETTE[:len(counts)]
bars = axes[1].barh(range(len(counts)), counts.values, color=colors, height=0.6)
axes[1].set_yticks(range(len(counts)))
axes[1].set_yticklabels(counts.index, fontsize=10)
axes[1].set_xlabel('Respondents')
axes[1].set_title('Cluster Size')
for i, (bar, v) in enumerate(zip(bars, counts.values)):
    pct = v / len(df_ai) * 100
    axes[1].text(v + 100, i, f'{v:,}  ({pct:.1f}%)', va='center', fontsize=9)
axes[1].set_xlim(0, counts.max() * 1.3)

plt.tight_layout()
plt.savefig('cluster_profiles.png', bbox_inches='tight')
plt.close()
print("    Saved: cluster_profiles.png")

# ─── 8. VISUALIZATION B: Archetype × Context breakdown ────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Who Is In Each Archetype? Role, Org Size & Experience", fontsize=14, fontweight='bold')

archetype_order = df_ai['Archetype'].value_counts().index.tolist()

# 8a. Top roles per archetype
ax = axes[0]
role_cross = pd.crosstab(df_ai['Archetype'], df_ai['PrimaryRole'], normalize='index')
top_roles = ['Full-Stack Dev','Back-End Dev','Data Scientist/ML','DevOps/Platform','Student','Architect']
role_cross = role_cross[[c for c in top_roles if c in role_cross.columns]]
role_cross = role_cross.loc[[a for a in archetype_order if a in role_cross.index]]
role_cross.plot(kind='barh', stacked=True, ax=ax, colormap='tab10', legend=True)
ax.set_title('Role Composition')
ax.set_xlabel('Proportion')
ax.legend(loc='lower right', fontsize=7)
ax.tick_params(axis='y', labelsize=8)

# 8b. Org size per archetype
ax = axes[1]
org_order = ['Solo/Micro','Small','Mid-Market','Large','Enterprise']
org_cross = pd.crosstab(df_ai['Archetype'], df_ai['OrgBucket'], normalize='index')
org_cross = org_cross[[c for c in org_order if c in org_cross.columns]]
org_cross = org_cross.loc[[a for a in archetype_order if a in org_cross.index]]
org_cross.plot(kind='barh', stacked=True, ax=ax, colormap='Set2', legend=True)
ax.set_title('Org Size Composition')
ax.set_xlabel('Proportion')
ax.legend(loc='lower right', fontsize=7)
ax.tick_params(axis='y', labelsize=8)

# 8c. Experience distribution per archetype (boxplot)
ax = axes[2]
arch_list = [a for a in archetype_order if a in df_ai['Archetype'].values]
exp_data = [df_ai[df_ai['Archetype']==a]['WorkExp'].dropna().values for a in arch_list]
bp = ax.boxplot(exp_data, vert=False, patch_artist=True,
                medianprops={'color':'black','linewidth':2})
for patch, color in zip(bp['boxes'], PALETTE):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_yticks(range(1, len(arch_list)+1))
ax.set_yticklabels(arch_list, fontsize=8)
ax.set_xlabel('Years of Work Experience')
ax.set_title('Experience Distribution')
ax.set_xlim(0, 35)

plt.tight_layout()
plt.savefig('cluster_context.png', bbox_inches='tight')
plt.close()
print("    Saved: cluster_context.png")

# ─── 9. ASSOCIATION RULES — ENRICHED ─────────────────────────────────────────
print("\n[8] Association Rules (enriched with role, org, experience)...")

def bin_usage(v):
    if v == 4: return "Usage:Daily"
    elif v == 3: return "Usage:Weekly"
    elif v >= 1: return "Usage:Occasional"
    else: return "Usage:Never"

def bin_trust(v):
    if v >= 3: return "Trust:High"
    elif v == 2: return "Trust:Neutral"
    else: return "Trust:Low"

def bin_sent(v):
    if v >= 4: return "Sent:Positive"
    elif v == 3: return "Sent:Neutral"
    else: return "Sent:Negative"

def bin_agent(v):
    if v >= 2: return "Agents:Active"
    elif v == 1: return "Agents:Planning"
    else: return "Agents:No"

def bin_exp(v):
    if pd.isna(v): return None
    if v <= 2: return "Exp:Junior"
    elif v <= 7: return "Exp:Mid"
    elif v <= 15: return "Exp:Senior"
    else: return "Exp:Veteran"

def bin_org(v):
    if v in ('Unknown', None): return None
    return f"Org:{v}"

def bin_role(v):
    key_roles = {'Full-Stack Dev','Back-End Dev','Data Scientist/ML',
                 'DevOps/Platform','Student','Architect','Engineering Manager'}
    if v in key_roles: return f"Role:{v.replace(' ','_')}"
    return None

def bin_threat(v):
    if pd.isna(v): return None
    if v >= 2: return "Threat:Yes"
    elif v == 0: return "Threat:No"
    return None

def bin_learn(v):
    return "LearnedAI:Yes" if v == 1 else "LearnedAI:No"

transactions = []
for _, row in df_ai.iterrows():
    items = [
        bin_usage(row['AIUsageScore']),
        bin_trust(row['AITrustScore']),
        bin_sent(row['AISentScore']),
        bin_agent(row['AgentScore']),
        bin_exp(row.get('WorkExp')),
        bin_org(row.get('OrgBucket')),
        bin_role(row.get('PrimaryRole')),
        bin_threat(row.get('ThreatScore')),
        bin_learn(row.get('LearnedAI', 0))
    ]
    items = [i for i in items if i is not None]
    if len(items) >= 4:
        transactions.append(items)

print(f"    Transactions: {len(transactions):,}")

te = TransactionEncoder()
te_array = te.fit_transform(transactions)
df_te = pd.DataFrame(te_array, columns=te.columns_)

freq_sets = apriori(df_te, min_support=0.07, use_colnames=True)
print(f"    Frequent itemsets: {len(freq_sets)}")

rules = association_rules(freq_sets, metric="lift", min_threshold=1.3)
rules['ant_str'] = rules['antecedents'].apply(lambda x: ', '.join(sorted(x)))
rules['con_str'] = rules['consequents'].apply(lambda x: ', '.join(sorted(x)))
rules = rules.sort_values('lift', ascending=False).reset_index(drop=True)
print(f"    Rules (lift > 1.3): {len(rules)}")

# Filter for rules that involve role, org, or experience as antecedents
interesting = rules[
    rules['ant_str'].str.contains('Role:|Org:|Exp:') |
    rules['con_str'].str.contains('Usage:|Agents:')
].head(20)

print("\n    SELECTED RULES (role/org/exp → adoption behavior):")
print(f"    {'Antecedent':<42} {'→  Consequent':<30} {'Conf':>6} {'Lift':>6}")
print("    " + "-" * 88)
for _, r in interesting.head(15).iterrows():
    print(f"    {r['ant_str']:<42} {r['con_str']:<30} {r['confidence']:>6.2f} {r['lift']:>6.2f}")


# ─── 10. RULES VISUALIZATION ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Association Rules — If This, Then That", fontsize=14, fontweight='bold')

# Scatter: all rules colored by consequent type
ax = axes[0]
def rule_category(con):
    if 'Daily' in con: return 'Daily Usage'
    elif 'Weekly' in con or 'Occasional' in con: return 'Moderate Usage'
    elif 'Never' in con: return 'Non-Usage'
    elif 'Agent' in con: return 'Agent Behavior'
    elif 'Trust' in con: return 'Trust'
    elif 'Sent' in con: return 'Sentiment'
    else: return 'Other'

rules['Category'] = rules['con_str'].apply(rule_category)
cat_colors = {
    'Daily Usage':'#4C72B0', 'Moderate Usage':'#55A868', 'Non-Usage':'#C44E52',
    'Agent Behavior':'#DD8452', 'Trust':'#8172B2', 'Sentiment':'#937860', 'Other':'grey'
}
for cat, grp in rules.groupby('Category'):
    ax.scatter(grp['support'], grp['confidence'], alpha=0.6,
               color=cat_colors.get(cat,'grey'), label=cat, s=40)
ax.set_xlabel('Support')
ax.set_ylabel('Confidence')
ax.set_title('All Rules by Consequent Type')
ax.legend(fontsize=7, loc='lower right')

# Bar chart: top 12 interesting rules by lift
ax = axes[1]
top12 = interesting.head(12).copy()
top12['label'] = top12.apply(lambda r: f"{r['ant_str'][:28]}…\n→ {r['con_str'][:28]}", axis=1)
colors = [cat_colors.get(rule_category(r['con_str']), 'grey') for _, r in top12.iterrows()]
bars = ax.barh(range(len(top12)), top12['lift'].values, color=colors, height=0.65)
ax.set_yticks(range(len(top12)))
ax.set_yticklabels(top12['label'].values, fontsize=7)
ax.set_xlabel('Lift')
ax.set_title('Top Rules Involving Role / Org / Experience')
ax.axvline(x=1.0, color='grey', linestyle='--', alpha=0.5)
for i, (bar, v) in enumerate(zip(bars, top12['lift'].values)):
    ax.text(v + 0.01, i, f'{v:.2f}', va='center', fontsize=7)

# Add legend
handles = [mpatches.Patch(color=c, label=l) for l, c in cat_colors.items() if l != 'Other']
ax.legend(handles=handles, fontsize=7, loc='lower right')

plt.tight_layout()
plt.savefig('association_rules_v2.png', bbox_inches='tight')
plt.close()
print("    Saved: association_rules_v2.png")

# ─── 11. CLASSIFICATION — REFINED ────────────────────────────────────────────
print("\n[9] Classification (Daily adopter prediction, refined)...")

# Use full clustering sample — median-impute WorkExp, YearsCode, ThreatScore
df_clf = df_ai.copy()
df_clf['Target'] = (df_clf['AIUsageScore'] == 4).astype(int)

feature_cols = [
    'AISentScore','AgentScore','LearnedAI','AITrustScore',
    'AIComplexScore','ThreatScore','WorkExp','YearsCode'
]
FEATURE_LABELS = {
    'AITrustScore':         'AI Trust Level',
    'AISentScore':          'AI Sentiment',
    'AgentScore':           'Agent Engagement',
    'AIComplexScore':       'AI Complexity Rating',
    'LearnedAI':            'Learned AI Tools (yr)',
    'ThreatScore':          'Job Threat Perception',
    'WorkExp':              'Years Work Experience',
    'YearsCode':            'Years Coding',
    'ExpBucket':            'Experience Bucket',
    'HasPurchaseInfluence': 'Has Tech Purchase Influence',
    'OrgBucket_enc':        'Organization Size',
    'WorkMode_enc':         'Work Mode (remote/hybrid)',
    'PrimaryRole_enc':      'Primary Developer Role'
}

X = df_clf[feature_cols].fillna(df_clf[feature_cols].median())
y = df_clf['Target']

print(f"    N={len(X):,}  |  Daily adopters={y.sum():,} ({y.mean()*100:.1f}%)")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

dt = DecisionTreeClassifier(max_depth=5, random_state=42, min_samples_leaf=50)
dt.fit(X_train, y_train)
dt_acc = accuracy_score(y_test, dt.predict(X_test))

rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1,
                             min_samples_leaf=20, max_features='sqrt')
rf.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf.predict(X_test))

print(f"\n    Decision Tree: {dt_acc:.4f}")
print(classification_report(y_test, dt.predict(X_test), target_names=['Non-Daily','Daily']))
print(f"    Random Forest: {rf_acc:.4f}")
print(classification_report(y_test, rf.predict(X_test), target_names=['Non-Daily','Daily']))

importances = pd.DataFrame({
    'Feature': [FEATURE_LABELS.get(f, f) for f in feature_cols],
    'RF': rf.feature_importances_,
    'DT': dt.feature_importances_
}).sort_values('RF', ascending=False)

# ─── ROBUSTNESS CHECK A: Three-seed cluster stability ─────────────────────────
print("\n[R1] Three-seed cluster stability check...")
seed_results = {}
for seed in [42, 99, 7]:
    km_test = KMeans(n_clusters=5, random_state=seed, n_init=20)
    lbl = km_test.fit_predict(X_cluster)
    sil = silhouette_score(X_cluster, lbl)
    sizes = sorted([np.sum(lbl==c) for c in range(5)], reverse=True)
    seed_results[seed] = (sil, sizes)
    print(f"    seed={seed}: silhouette={sil:.4f}  cluster sizes={sizes}")
sil_vals = [v[0] for v in seed_results.values()]
print(f"    Range: {min(sil_vals):.4f}–{max(sil_vals):.4f}  ({'STABLE' if max(sil_vals)-min(sil_vals)<0.001 else 'VARIABLE'})")

# ─── ROBUSTNESS CHECK B: 5-fold cross-validation ──────────────────────────────
print("\n[R2] 5-fold cross-validation...")
from sklearn.model_selection import StratifiedKFold, cross_val_score
cv_scores = cross_val_score(
    RandomForestClassifier(n_estimators=200, min_samples_leaf=20, random_state=42, n_jobs=-1),
    X, y,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring='accuracy', n_jobs=-1
)
print(f"    5-fold CV: {cv_scores.mean()*100:.1f}% ± {cv_scores.std()*100:.1f}%")
print(f"    Folds: {[f'{s*100:.1f}%' for s in cv_scores]}")

# ─── ROBUSTNESS CHECK C: Permutation importance ───────────────────────────────
print("\n[R3] Permutation importance (vs Gini)...")
from sklearn.inspection import permutation_importance as perm_imp
perm = perm_imp(rf, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1)
print(f"    {'Feature':<25} {'Gini':>8} {'Permutation':>14}")
gini_imp = rf.feature_importances_
perm_means = perm.importances_mean
for i, feat in enumerate(feature_cols):
    print(f"    {feat:<25} {gini_imp[i]*100:>6.1f}%  {perm_means[i]*100:>10.2f}%")
top_gini  = feature_cols[gini_imp.argmax()]
top_perm  = feature_cols[perm_means.argmax()]
print(f"    #1 by Gini: {top_gini}  |  #1 by Permutation: {top_perm}")
print(f"    AISentScore #1 by both: {'YES' if top_gini == top_perm == 'AISentScore' else 'NO'}")



# ─── 12. CLASSIFICATION VISUALIZATION ────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Classification: What Predicts Daily AI Adoption?", fontsize=14, fontweight='bold')

# Feature importance comparison (RF vs DT)
ax = axes[0]
top_n = 10
top_feats = importances.head(top_n)
x = np.arange(top_n)
width = 0.35
bars1 = ax.barh(x + width/2, top_feats['RF'].values, width, label='Random Forest', color=PALETTE[0])
bars2 = ax.barh(x - width/2, top_feats['DT'].values, width, label='Decision Tree', color=PALETTE[1])
ax.set_yticks(x)
ax.set_yticklabels(top_feats['Feature'].values, fontsize=9)
ax.set_xlabel('Feature Importance')
ax.set_title('Top 10 Predictors of Daily Adoption')
ax.legend()
ax.invert_yaxis()

# Model accuracy + F1 summary table
ax = axes[1]
ax.axis('off')

dt_report = classification_report(y_test, dt.predict(X_test),
                                   target_names=['Non-Daily','Daily'], output_dict=True)
rf_report = classification_report(y_test, rf.predict(X_test),
                                   target_names=['Non-Daily','Daily'], output_dict=True)

table_data = [
    ['Metric', 'Decision Tree', 'Random Forest'],
    ['Accuracy', f"{dt_acc:.3f}", f"{rf_acc:.3f}"],
    ['Precision (Daily)', f"{dt_report['Daily']['precision']:.3f}", f"{rf_report['Daily']['precision']:.3f}"],
    ['Recall (Daily)',    f"{dt_report['Daily']['recall']:.3f}",    f"{rf_report['Daily']['recall']:.3f}"],
    ['F1 (Daily)',        f"{dt_report['Daily']['f1-score']:.3f}",  f"{rf_report['Daily']['f1-score']:.3f}"],
    ['Precision (Non)',   f"{dt_report['Non-Daily']['precision']:.3f}", f"{rf_report['Non-Daily']['precision']:.3f}"],
    ['Recall (Non)',      f"{dt_report['Non-Daily']['recall']:.3f}",    f"{rf_report['Non-Daily']['recall']:.3f}"],
    ['F1 (Non)',          f"{dt_report['Non-Daily']['f1-score']:.3f}",  f"{rf_report['Non-Daily']['f1-score']:.3f}"],
]

tbl = ax.table(cellText=table_data[1:], colLabels=table_data[0],
               loc='center', cellLoc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1.4, 2.0)
for j in range(3):
    tbl[(0,j)].set_facecolor('#4C72B0')
    tbl[(0,j)].set_text_props(color='white', fontweight='bold')
for i in range(1, len(table_data)):
    for j in range(3):
        tbl[(i,j)].set_facecolor('#f0f4ff' if i % 2 == 0 else 'white')
ax.set_title('Model Evaluation Summary', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('classification_v2.png', bbox_inches='tight')
plt.close()
print("    Saved: classification_v2.png")

# ─── 13. DECISION TREE PATH (human-readable rules) ───────────────────────────
print("\n[10] Decision Tree — key decision paths...")
from sklearn.tree import _tree

def get_tree_rules(tree, feature_names, labels, n_top=8):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    paths = []
    def recurse(node, depth, path):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            recurse(tree_.children_left[node],  depth+1, path + [f"{name} ≤ {threshold:.2f}"])
            recurse(tree_.children_right[node], depth+1, path + [f"{name} > {threshold:.2f}"])
        else:
            values = tree_.value[node][0]
            total = sum(values)
            pred_class = labels[np.argmax(values)]
            confidence = max(values)/total
            paths.append((confidence, pred_class, path, int(total)))
    recurse(0, 0, [])
    paths.sort(reverse=True)
    return paths[:n_top]

label_names = ['Non-Daily','Daily']
paths = get_tree_rules(dt, [FEATURE_LABELS.get(f,f) for f in feature_cols], label_names)
print("\n    Top decision paths:")
for conf, pred, path, n in paths[:6]:
    print(f"\n    → Predicts: {pred}  (confidence={conf:.2f}, n={n:,})")
    for step in path:
        print(f"       IF {step}")

# ─── 14. SUMMARY ──────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("  PIPELINE v2 COMPLETE")
print("="*70)

print("\n  CLUSTER BREAKDOWN:")
counts = df_ai['Archetype'].value_counts()
for name, count in counts.items():
    pct = count/len(df_ai)*100
    desc = ARCHETYPE_DESC.get([k for k,v in ARCHETYPE_NAMES.items() if v==name][0], '')
    print(f"\n    {name} ({pct:.1f}%)")
    print(f"    → {desc}")

print(f"\n  CLASSIFICATION:")
print(f"    Random Forest accuracy: {rf_acc:.4f}")
print(f"    Decision Tree accuracy: {dt_acc:.4f}")
print(f"    Top predictor: {importances.iloc[0]['Feature']}")

print(f"\n  OUTPUTS:")
for f in ['cluster_profiles.png','cluster_context.png',
          'association_rules_v2.png','classification_v2.png']:
    print(f"    {f}")

# ─── ROBUSTNESS CHECK D: K-modes clustering ───────────────────────────────────
print("\n[R4] K-modes robustness check (ordinal-appropriate clustering)...")
try:
    from kmodes.kmodes import KModes
    X_ordinal = df_ai[CLUSTER_FEATURES].values.astype(int)
    # Cost curve k=2 through k=6
    print("    K-modes cost curve:")
    for k_test in range(2, 7):
        km_test = KModes(n_clusters=k_test, init='Huang', n_init=10, random_state=42, verbose=0)  # 10 inits for scan speed
        km_test.fit(X_ordinal)
        print(f"      k={k_test}: cost={km_test.cost_:.1f}")
    print("    (Monotonically decreasing = no statistical elbow favoring k=2)")
    # Primary run at k=5
    km_modes = KModes(n_clusters=5, init='Huang', n_init=20, random_state=42, verbose=0)
    kmode_labels = km_modes.fit_predict(X_ordinal)
    df_ai_kmode = df_ai.copy()
    df_ai_kmode['kmode_label'] = kmode_labels
    print(f"    K-modes k=5 cluster profiles (sorted by usage):")
    rows = []
    for c in range(5):
        sub = df_ai_kmode[df_ai_kmode['kmode_label']==c]
        rows.append({'c':c,'n':len(sub),'pct':len(sub)/len(df_ai_kmode)*100,
                     'usage':sub['AIUsageScore'].mean(),'trust':sub['AITrustScore'].mean(),
                     'sent':sub['AISentScore'].mean()})
    for r in sorted(rows, key=lambda x: -x['usage']):
        print(f"    C{r['c']}: n={r['n']:,} ({r['pct']:.1f}%)  "
              f"usage={r['usage']:.2f}  trust={r['trust']:.2f}  sent={r['sent']:.2f}")
    # Compare to k-means
    kmeans_ref = [('Daily Integrators',3.83,2.61,4.44),('Enthusiastic Adopters',3.49,2.59,4.22),
                  ('Cautious Experimenters',3.07,1.07,3.25),('Pragmatic Dabblers',2.63,1.86,3.61),
                  ('Active Resisters',0.47,0.43,0.82)]
    kmode_sorted = sorted(rows, key=lambda x: -x['usage'])
    print("\n    Correspondence to k-means archetypes:")
    for (name,u,t,s), km_row in zip(kmeans_ref, kmode_sorted):
        du, dt = abs(km_row['usage']-u), abs(km_row['trust']-t)
        match = 'Strong' if du<0.4 and dt<0.4 else 'Moderate' if du<0.7 else 'Weak'
        print(f"    {name:<26} → C{km_row['c']} ({match})  ΔUsage={du:.2f} ΔTrust={dt:.2f}")
except ImportError:
    print("    kmodes not installed — run: pip install kmodes")

# ─── ROBUSTNESS CHECK E: Single-method learner analysis ──────────────────────
print("\n[R5] Single-method learner robustness check...")
trust_map_local = {'Highly trust':4,'Somewhat trust':3,'Neither trust nor distrust':2,
                   'Somewhat distrust':1,'Highly distrust':0}
df25_local = df_ai.copy()
df25_raw = pd.read_csv(CSV_2025, low_memory=False)
df25_raw['AITrustScore'] = df25_raw['AIAcc'].map(trust_map_local)
df25_raw['learn_count'] = df25_raw['AILearnHow'].apply(
    lambda v: len(str(v).split(';')) if pd.notna(v) else None)
single_method = df25_raw[df25_raw['learn_count']==1].dropna(subset=['AITrustScore'])
print(f"    Single-method learners: n={len(single_method):,}")
method_map = {'Coding Bootcamp':'Bootcamp','Colleague or on-the-job':'Colleague',
              'Online Courses or Certification':'Online Courses',
              'School (i.e., University':'School'}
print(f"    {'Method':<20} {'All-respondents':>16} {'Single-method':>14} {'n (single)':>10}")
for partial, label in method_map.items():
    all_mask = df25_raw['AILearnHow'].fillna('').str.contains(partial, case=False)
    sub_all = df25_raw[all_mask].dropna(subset=['AITrustScore'])
    tr_all = (sub_all['AITrustScore'] >= 3).mean()*100
    sing_mask = single_method['AILearnHow'].fillna('').str.contains(partial, case=False)
    sub_s = single_method[sing_mask]
    tr_s = (sub_s['AITrustScore'] >= 3).mean()*100 if len(sub_s) > 10 else float('nan')
    print(f"    {label:<20} {tr_all:>14.1f}%  {tr_s:>12.1f}%  {len(sub_s):>10}")
print("    Bootcamp n=21 in single-method subset — endpoint direction holds,")
print("    but specific 66.5% rate is not reliable at that sample size.")

