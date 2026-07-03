"""
Prepares Tableau-ready data from the original Unicorn_Companies.csv.
Outputs two tidy CSVs:
  1. unicorns_main.csv       — one row per company, cleaned + derived columns
  2. unicorns_investors.csv  — long format, one row per company-investor pair
"""
import pandas as pd
import numpy as np
import os

SRC = "/Users/ziyaoxiao/Desktop/肖梓耀/Cornell/Capstone Project/Data/Unicorn_Companies.csv"
OUT = "/Users/ziyaoxiao/Desktop/肖梓耀/Cornell/Capstone Project/dashboard"
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(SRC)
print(f"Loaded {len(df)} rows.")

# ── 1. clean industry capitalization (merge AI variants) ────────────────────
canon = {}
for name in df['Industry'].unique():
    key = name.lower()
    if key not in canon:
        canon[key] = name
df['Industry'] = df['Industry'].apply(lambda s: canon[s.lower()])

# ── 2. parse dollar strings to numeric USD ──────────────────────────────────
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

# readable scaled versions
df['Valuation_B'] = (df['Valuation_USD'] / 1e9).round(2)
df['Funding_M']   = (df['Funding_USD'] / 1e6).round(1)

# ── 3. dates & derived time columns ─────────────────────────────────────────
df['Date_Joined']       = pd.to_datetime(df['Date Joined'])
df['Year_Joined']       = df['Date_Joined'].dt.year
df['Year_Founded']      = df['Year Founded']
df['Years_to_Unicorn']  = df['Year_Joined'] - df['Year_Founded']

# ── 4. capital efficiency (valuation per $ raised) ──────────────────────────
df['Capital_Multiple'] = np.where(
    (df['Funding_USD'] > 0) & df['Funding_USD'].notna(),
    (df['Valuation_USD'] / df['Funding_USD']).round(1),
    np.nan
)

# ── 5. valuation tier & decacorn flag ───────────────────────────────────────
def val_tier(v):
    if pd.isna(v): return np.nan
    b = v / 1e9
    if b < 2:   return '1. $1-2B'
    if b < 5:   return '2. $2-5B'
    if b < 10:  return '3. $5-10B'
    return '4. $10B+ (Decacorn)'
df['Valuation_Tier'] = df['Valuation_USD'].apply(val_tier)
df['Is_Decacorn']    = (df['Valuation_USD'] >= 10e9).astype(int)

# ── 6. founding era (technology wave) ───────────────────────────────────────
def era(y):
    if pd.isna(y):   return np.nan
    if y <= 2000:    return '1. Dot-Com & Early Web (<=2000)'
    if y <= 2008:    return '2. Web 2.0 & Social (2001-2008)'
    if y <= 2014:    return '3. Mobile & Cloud (2009-2014)'
    return '4. AI & Modern Stack (2015-2021)'
df['Founding_Era'] = df['Year_Founded'].apply(era)

# ── 7. legacy flag (pre-2000 non-startup outliers) ──────────────────────────
df['Legacy_Pre2000'] = (df['Year_Founded'] <= 2000).astype(int)

# ── 8. investor count ───────────────────────────────────────────────────────
def count_inv(s):
    if pd.isna(s): return 0
    return len([x for x in str(s).split(',') if x.strip()])
df['Num_Investors'] = df['Select Investors'].apply(count_inv)

# ── 9. handle duplicate company names ───────────────────────────────────────
dups = df[df.duplicated('Company', keep=False)].sort_values('Company')
if len(dups):
    print(f"\nDuplicate company name(s) found: {dups['Company'].unique().tolist()}")
    print(dups[['Company', 'Country', 'Industry', 'Valuation_B']].to_string(index=False))
# drop only fully-identical rows; keep same-name-different-company rows
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df)} fully-identical duplicate row(s).")

# ── 10. assemble & save MAIN table ──────────────────────────────────────────
main_cols = [
    'Company', 'Industry', 'City', 'Country', 'Continent',
    'Year_Founded', 'Founding_Era', 'Legacy_Pre2000',
    'Date_Joined', 'Year_Joined', 'Years_to_Unicorn',
    'Valuation_USD', 'Valuation_B', 'Valuation_Tier', 'Is_Decacorn',
    'Funding_USD', 'Funding_M', 'Capital_Multiple',
    'Num_Investors', 'Select Investors',
]
main = df[main_cols].rename(columns={'Select Investors': 'Select_Investors'})
main.to_csv(f'{OUT}/unicorns_main.csv', index=False)
print(f"\nSaved unicorns_main.csv  ({len(main)} rows, {len(main.columns)} cols)")

# ── 11. build & save INVESTORS long table ───────────────────────────────────
rows = []
for _, r in df.iterrows():
    if pd.isna(r['Select Investors']):
        continue
    for inv in str(r['Select Investors']).split(','):
        inv = inv.strip()
        if inv:
            rows.append({
                'Company': r['Company'],
                'Investor': inv,
                'Industry': r['Industry'],
                'Country': r['Country'],
                'Continent': r['Continent'],
                'Valuation_B': r['Valuation_B'],
                'Year_Joined': r['Year_Joined'],
                'Is_Decacorn': r['Is_Decacorn'],
            })
inv_df = pd.DataFrame(rows)
inv_df.to_csv(f'{OUT}/unicorns_investors.csv', index=False)
print(f"Saved unicorns_investors.csv  ({len(inv_df)} rows, "
      f"{inv_df['Investor'].nunique()} unique investors)")

# ── 12. quick sanity summary ────────────────────────────────────────────────
print("\n--- Sanity checks ---")
print(f"Companies: {len(main)}")
print(f"Decacorns: {main['Is_Decacorn'].sum()}")
print(f"Median valuation: ${main['Valuation_B'].median():.1f}B")
print(f"Median capital multiple: {main['Capital_Multiple'].median():.1f}x")
print(f"Investor-company pairs: {len(inv_df)}")
print(f"Top investor: {inv_df['Investor'].value_counts().index[0]} "
      f"({inv_df['Investor'].value_counts().iloc[0]} companies)")
