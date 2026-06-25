import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ── style ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
})

COLORS = {
    'primary':   '#2563EB',
    'secondary': '#7C3AED',
    'accent':    '#059669',
    'warm':      '#DC2626',
    'muted':     '#64748B',
    'palette':   ['#2563EB','#7C3AED','#059669','#DC2626','#D97706',
                  '#0891B2','#BE185D','#65A30D','#9333EA','#EA580C',
                  '#0D9488','#4F46E5','#B45309','#6B7280','#1D4ED8'],
}

OUT = "/Users/ziyaoxiao/Desktop/肖梓耀/Cornell/Capstone Project/descriptive analysis"

# ── load & clean ───────────────────────────────────────────────────────────
df = pd.read_csv(
    "/Users/ziyaoxiao/Desktop/肖梓耀/Cornell/Capstone Project/Data/Unicorn_Companies.csv"
)

def parse_dollar(s):
    s = str(s).strip().replace('$', '').replace(',', '')
    if s.endswith('B'):
        return float(s[:-1]) * 1e9
    if s.endswith('M'):
        return float(s[:-1]) * 1e6
    try:
        return float(s)
    except Exception:
        return np.nan

df['Valuation_USD'] = df['Valuation'].apply(parse_dollar)
df['Funding_USD']   = df['Funding'].apply(parse_dollar)
df['Date Joined']   = pd.to_datetime(df['Date Joined'])
df['Year Joined']   = df['Date Joined'].dt.year

# data cleaning: merge inconsistent industry capitalization
# (e.g. "Artificial Intelligence" vs "Artificial intelligence")
ind_canonical = {}
for name in df['Industry'].unique():
    key = name.lower()
    if key not in ind_canonical:
        ind_canonical[key] = name  # keep first-seen spelling
df['Industry'] = df['Industry'].apply(lambda s: ind_canonical[s.lower()])

total = len(df)
print(f"Total unicorn companies: {total}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 – Geographic Distribution
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Geographic Distribution of Unicorn Companies', fontsize=15, fontweight='bold', y=1.01)

# 1a – Continent bar chart
cont = df['Continent'].value_counts()
ax = axes[0]
bars = ax.barh(cont.index[::-1], cont.values[::-1], color=COLORS['palette'][:len(cont)], edgecolor='white')
for bar, val in zip(bars, cont.values[::-1]):
    pct = val / total * 100
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            f'{val:,}  ({pct:.1f}%)', va='center', fontsize=10)
ax.set_xlabel('Number of Unicorns')
ax.set_title('By Continent')
ax.set_xlim(0, cont.max() * 1.28)

# 1b – Top 15 countries
top_countries = df['Country'].value_counts().head(15)
ax2 = axes[1]
bars2 = ax2.barh(top_countries.index[::-1], top_countries.values[::-1],
                 color=COLORS['primary'], alpha=0.85, edgecolor='white')
for bar, val in zip(bars2, top_countries.values[::-1]):
    pct = val / total * 100
    ax2.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
             f'{val:,}  ({pct:.1f}%)', va='center', fontsize=9)
ax2.set_xlabel('Number of Unicorns')
ax2.set_title('Top 15 Countries')
ax2.set_xlim(0, top_countries.max() * 1.32)

plt.tight_layout()
plt.savefig(f'{OUT}/01_geographic_distribution.png', bbox_inches='tight')
plt.close()
print("Saved: 01_geographic_distribution.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 – Industry Distribution
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 7))
ind = df['Industry'].value_counts()
bars = ax.barh(ind.index[::-1], ind.values[::-1],
               color=COLORS['palette'][:len(ind)], edgecolor='white')
for bar, val in zip(bars, ind.values[::-1]):
    pct = val / total * 100
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{val:,}  ({pct:.1f}%)', va='center', fontsize=10)
ax.set_xlabel('Number of Unicorns')
ax.set_title('Industry Distribution of Unicorn Companies', fontsize=14, fontweight='bold')
ax.set_xlim(0, ind.max() * 1.3)
plt.tight_layout()
plt.savefig(f'{OUT}/02_industry_distribution.png', bbox_inches='tight')
plt.close()
print("Saved: 02_industry_distribution.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 – Valuation Distribution
# ══════════════════════════════════════════════════════════════════════════════
val_b = df['Valuation_USD'].dropna() / 1e9  # in billions

# valuation bracket bar chart (no log scale)
brackets = [1, 2, 5, 10, 20, 50, float('inf')]
labels   = ['$1-2B','$2-5B','$5-10B','$10-20B','$20-50B','$50B+']
val_b_series = val_b.dropna()
counts = [((val_b_series >= brackets[i]) & (val_b_series < brackets[i+1])).sum()
          for i in range(len(labels))]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(labels, counts, color=COLORS['palette'][:len(labels)], edgecolor='white')
for bar, cnt in zip(bars, counts):
    pct = cnt / len(val_b_series) * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            f'{cnt}\n({pct:.1f}%)', ha='center', fontsize=10)
ax.set_xlabel('Valuation Bracket')
ax.set_ylabel('Number of Companies')
ax.set_title('Valuation Distribution of Unicorn Companies', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(counts) * 1.12)

plt.tight_layout()
plt.savefig(f'{OUT}/03_valuation_distribution.png', bbox_inches='tight')
plt.close()
print("Saved: 03_valuation_distribution.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 – Funding Distribution
# ══════════════════════════════════════════════════════════════════════════════
fund_b = df['Funding_USD'].dropna() / 1e9

# funding bracket bar chart (no log scale)
brackets_f = [0, 0.1, 0.5, 1, 2, 5, float('inf')]
labels_f   = ['<$100M','$100-500M','$500M-1B','$1-2B','$2-5B','$5B+']
counts_f = [((fund_b >= brackets_f[i]) & (fund_b < brackets_f[i+1])).sum()
            for i in range(len(labels_f))]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(labels_f, counts_f, color=COLORS['palette'][:len(labels_f)], edgecolor='white')
for bar, cnt in zip(bars, counts_f):
    pct = cnt / len(fund_b) * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            f'{cnt}\n({pct:.1f}%)', ha='center', fontsize=10)
ax.set_xlabel('Funding Bracket')
ax.set_ylabel('Number of Companies')
ax.set_title('Funding Distribution of Unicorn Companies', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(counts_f) * 1.12)

plt.tight_layout()
plt.savefig(f'{OUT}/04_funding_distribution.png', bbox_inches='tight')
plt.close()
print("Saved: 04_funding_distribution.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 – Founding Year & Year Joined Timeline
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle('Company Age & Unicorn Entry Timing', fontsize=14, fontweight='bold')

# 5a – Year Founded
ax = axes[0]
yr_counts = df['Year Founded'].value_counts().sort_index()
yr_counts = yr_counts[yr_counts.index >= 1995]
ax.bar(yr_counts.index, yr_counts.values, color=COLORS['accent'], alpha=0.85, edgecolor='white')
ax.set_xlabel('Year Founded')
ax.set_ylabel('Number of Companies')
ax.set_title('Year Founded Distribution')

# 5b – Year became unicorn
ax2 = axes[1]
yj_counts = df['Year Joined'].value_counts().sort_index()
ax2.bar(yj_counts.index, yj_counts.values, color=COLORS['warm'], alpha=0.85, edgecolor='white')
ax2.set_xlabel('Year Became Unicorn')
ax2.set_ylabel('Number of Companies')
ax2.set_title('Year Became Unicorn')

plt.tight_layout()
plt.savefig(f'{OUT}/05_timeline.png', bbox_inches='tight')
plt.close()
print("Saved: 05_timeline.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 – Years to Become a Unicorn
# ══════════════════════════════════════════════════════════════════════════════
df['Years_to_Unicorn'] = df['Year Joined'] - df['Year Founded']
ytu = df['Years_to_Unicorn'].dropna()
ytu = ytu[ytu >= 0]

fig, ax = plt.subplots(figsize=(12, 5))
ax.hist(ytu, bins=range(0, int(ytu.max()) + 2), color=COLORS['primary'],
        alpha=0.85, edgecolor='white', align='left')
ax.axvline(ytu.median(), color=COLORS['warm'], linewidth=2, linestyle='--',
           label=f'Median: {ytu.median():.0f} yrs')
ax.axvline(ytu.mean(), color=COLORS['secondary'], linewidth=2, linestyle=':',
           label=f'Mean: {ytu.mean():.1f} yrs')
ax.set_xlabel('Years from Founding to Unicorn Status')
ax.set_ylabel('Number of Companies')
ax.set_title('How Long Does It Take to Become a Unicorn?', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{OUT}/06_years_to_unicorn.png', bbox_inches='tight')
plt.close()
print("Saved: 06_years_to_unicorn.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 7 – Industry × Continent Heatmap
# ══════════════════════════════════════════════════════════════════════════════
top_ind  = df['Industry'].value_counts().head(10).index
top_cont = ['North America', 'Asia', 'Europe', 'South America']
sub = df[df['Industry'].isin(top_ind) & df['Continent'].isin(top_cont)]
ct  = pd.crosstab(sub['Industry'], sub['Continent'])
ct  = ct.reindex(columns=top_cont, fill_value=0)
ct  = ct.loc[ct.sum(axis=1).sort_values(ascending=False).index]

fig, ax = plt.subplots(figsize=(10, 7))
im = ax.imshow(ct.values, aspect='auto', cmap='Blues')
plt.colorbar(im, ax=ax, label='Number of Unicorns')
ax.set_xticks(range(len(top_cont)))
ax.set_xticklabels(top_cont, fontsize=11)
ax.set_yticks(range(len(ct.index)))
ax.set_yticklabels(ct.index, fontsize=10)
for i in range(len(ct.index)):
    for j in range(len(top_cont)):
        val = ct.values[i, j]
        color = 'white' if val > ct.values.max() * 0.6 else 'black'
        ax.text(j, i, str(val), ha='center', va='center', fontsize=11,
                fontweight='bold', color=color)
ax.set_title('Industry × Continent Heatmap (Top 10 Industries)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{OUT}/07_industry_continent_heatmap.png', bbox_inches='tight')
plt.close()
print("Saved: 07_industry_continent_heatmap.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 8 – Technological Eras: how the unicorn industry mix shifted by the
#            company's FOUNDING year. Eras are framed around the dominant tech
#            wave of each period.
# ══════════════════════════════════════════════════════════════════════════════
era_bins   = [1900, 2000, 2008, 2014, 2025]
era_labels = ['Dot-Com &\nEarly Web\n(≤2000)',
              'Web 2.0 &\nSocial\n(2001-2008)',
              'Mobile &\nCloud\n(2009-2014)',
              'AI &\nModern Stack\n(2015-2021)']
df['Era'] = pd.cut(df['Year Founded'], bins=era_bins, labels=era_labels)

era_sizes = df['Era'].value_counts().reindex(era_labels)

# industry share (%) within each era, for the leading industries
focus_inds = ['Fintech', 'Internet software & services',
              'E-commerce & direct-to-consumer', 'Artificial intelligence',
              'Health', 'Cybersecurity']
share = (df.groupby('Era')['Industry']
           .value_counts(normalize=True)
           .mul(100)
           .rename('pct')
           .reset_index())
pivot = share.pivot(index='Era', columns='Industry', values='pct').reindex(era_labels)

fig, axes = plt.subplots(1, 2, figsize=(18, 7),
                         gridspec_kw={'width_ratios': [1, 1.5]})
fig.suptitle('Unicorns Across Technological Eras (by Founding Year)',
             fontsize=16, fontweight='bold', y=1.02)

# 8a – how many unicorns were founded in each era
ax = axes[0]
bars = ax.bar(range(len(era_labels)), era_sizes.values,
              color=COLORS['palette'][:len(era_labels)], edgecolor='white')
for bar, val in zip(bars, era_sizes.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{val}\n({val/total*100:.1f}%)', ha='center', fontsize=10)
ax.set_xticks(range(len(era_labels)))
ax.set_xticklabels(era_labels, fontsize=9)
ax.set_ylabel('Number of Unicorns Founded')
ax.set_title('Unicorns by Founding Era')
ax.set_ylim(0, era_sizes.max() * 1.15)

# 8b – industry-share evolution across the eras (line per industry)
ax2 = axes[1]
era_x = range(len(era_labels))
for i, ind in enumerate(focus_inds):
    if ind in pivot.columns:
        ax2.plot(era_x, pivot[ind].values, marker='o', linewidth=2.5,
                 markersize=8, color=COLORS['palette'][i], label=ind)
ax2.set_xticks(list(era_x))
ax2.set_xticklabels(era_labels, fontsize=9)
ax2.set_ylabel('Share of Unicorns Within Era (%)')
ax2.set_title('Industry Mix Shift Across Eras')
ax2.legend(fontsize=9, loc='upper left', framealpha=0.9)
ax2.grid(axis='y', alpha=0.25)

plt.tight_layout()
plt.savefig(f'{OUT}/08_technological_eras.png', bbox_inches='tight')
plt.close()
print("Saved: 08_technological_eras.png")

print("\nAll charts saved to:", OUT)
