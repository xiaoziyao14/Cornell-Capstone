"""
Generates the data-driven insight charts (figures 9-11) that support the
independent exploratory analysis. Run after unicorn_descriptive.py.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'figure.dpi': 150,
})
PAL = ['#2563EB','#7C3AED','#059669','#DC2626','#D97706','#0891B2',
       '#BE185D','#65A30D','#9333EA','#EA580C','#0D9488','#4F46E5',
       '#B45309','#6B7280','#1D4ED8']
OUT = "/Users/ziyaoxiao/Desktop/肖梓耀/Cornell/Capstone Project/descriptive analysis"

# ── load & clean ───────────────────────────────────────────────────────────
df = pd.read_csv("/Users/ziyaoxiao/Desktop/肖梓耀/Cornell/Capstone Project/Data/Unicorn_Companies.csv")
canon = {}
for n in df['Industry'].unique():
    k = n.lower()
    if k not in canon:
        canon[k] = n
df['Industry'] = df['Industry'].apply(lambda s: canon[s.lower()])

def parse_dollar(s):
    s = str(s).replace('$', '').replace(',', '')
    if s.endswith('B'): return float(s[:-1]) * 1e9
    if s.endswith('M'): return float(s[:-1]) * 1e6
    try: return float(s)
    except: return np.nan

df['V'] = df['Valuation'].apply(parse_dollar)
df['F'] = df['Funding'].apply(parse_dollar)
df['eff'] = df['V'] / df['F']


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 9 – Capital Efficiency by Industry (median Valuation / Funding)
# ══════════════════════════════════════════════════════════════════════════════
valid = df[(df['F'] > 0) & df['F'].notna() & df['V'].notna()]
eff_ind = valid.groupby('Industry')['eff'].median().sort_values()

fig, ax = plt.subplots(figsize=(11, 7))
colors = ['#DC2626' if v < 4 else '#D97706' if v < 5.5 else '#059669'
          for v in eff_ind.values]
bars = ax.barh(eff_ind.index, eff_ind.values, color=colors, edgecolor='white')
for bar, v in zip(bars, eff_ind.values):
    ax.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height()/2,
            f'{v:.1f}x', va='center', fontsize=10)
ax.axvline(valid['eff'].median(), color='#334155', linestyle='--', linewidth=1.5,
           label=f"Overall median: {valid['eff'].median():.1f}x")
ax.set_xlabel('Median Valuation / Funding (x)')
ax.set_title('Capital Efficiency by Industry\n(higher = more valuation per $ raised)',
             fontsize=13, fontweight='bold')
ax.set_xlim(0, eff_ind.max() * 1.15)
ax.legend(loc='lower right', fontsize=10)
plt.tight_layout()
plt.savefig(f'{OUT}/09_capital_efficiency.png', bbox_inches='tight')
plt.close()
print("Saved: 09_capital_efficiency.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 10 – Country Industry Specialization (share of each country's #1 sector)
# ══════════════════════════════════════════════════════════════════════════════
countries = ['United Kingdom','Israel','India','China','United States','Germany','France']
rows = []
for c in countries:
    sub = df[df['Country'] == c]
    top = sub['Industry'].value_counts()
    rows.append((c, top.index[0], top.iloc[0] / len(sub) * 100, len(sub)))
spec = pd.DataFrame(rows, columns=['Country','TopIndustry','Share','N']).sort_values('Share')

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(range(len(spec)), spec['Share'], color=PAL[:len(spec)], edgecolor='white')
for i, (bar, row) in enumerate(zip(bars, spec.itertuples())):
    ax.text(bar.get_width() + 0.8, i, f'{row.Share:.0f}%  —  {row.TopIndustry}',
            va='center', fontsize=10)
ax.set_yticks(range(len(spec)))
ax.set_yticklabels([f'{r.Country}\n(n={r.N})' for r in spec.itertuples()], fontsize=10)
ax.set_xlabel("Share of the Country's Unicorns in Its #1 Industry (%)")
ax.set_title('National Industry Specialization\n(how concentrated each country is in one sector)',
             fontsize=13, fontweight='bold')
ax.set_xlim(0, 75)
plt.tight_layout()
plt.savefig(f'{OUT}/10_country_specialization.png', bbox_inches='tight')
plt.close()
print("Saved: 10_country_specialization.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 11 – Funding vs Valuation scatter (weak correlation)
# ══════════════════════════════════════════════════════════════════════════════
sc = df[['V','F','Industry']].dropna()
sc = sc[(sc['F'] > 0) & (sc['V'] > 0)]
corr = np.log(sc['V']).corr(np.log(sc['F']))

fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(sc['F']/1e6, sc['V']/1e9, s=28, alpha=0.4, color='#2563EB', edgecolor='none')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('Total Funding (Million USD, log)')
ax.set_ylabel('Valuation (Billion USD, log)')
ax.set_title(f'Funding vs. Valuation — Weak Link (log-log r = {corr:.2f})\n'
             f'Money raised explains only ~{corr**2*100:.0f}% of valuation variance',
             fontsize=13, fontweight='bold')
# reference line: median efficiency multiple
med_eff = (sc['V']/sc['F']).median()
xs = np.array([sc['F'].min(), sc['F'].max()])
ax.plot(xs/1e6, (xs*med_eff)/1e9, color='#DC2626', linestyle='--',
        label=f'Median {med_eff:.1f}x line')
ax.legend(fontsize=10)
ax.grid(alpha=0.2, which='both')
plt.tight_layout()
plt.savefig(f'{OUT}/11_funding_vs_valuation.png', bbox_inches='tight')
plt.close()
print("Saved: 11_funding_vs_valuation.png")

print("Insight charts done.")
