# Unicorn Dashboard — Data & Build Guide

Tableau-ready data prepared from the original `Data/Unicorn_Companies.csv`
(CB Insights snapshot, ~April 2022; 1,074 unicorns).

Run `python3 prepare_tableau_data.py` to regenerate the two CSVs below.

---

## Files

| File | Grain | Rows | Use for |
|------|-------|------|---------|
| `unicorns_main.csv` | one row per company | 1,074 | all company-level views (geography, industry, valuation, trends) |
| `unicorns_investors.csv` | one row per company–investor pair | 3,051 | investor views (top investors, who backs which sector/geo) |

In Tableau, relate the two tables on **Company** (or use them as separate data sources).

---

## Data Dictionary — `unicorns_main.csv`

| Column | Meaning |
|--------|---------|
| `Company` | Company name (note: two distinct firms named "Bolt" — Estonia/mobility & US/fintech) |
| `Industry` | Sector (AI capitalization variants merged into one category) |
| `City`, `Country`, `Continent` | Location (City missing for 16 companies) |
| `Year_Founded` | Founding year |
| `Founding_Era` | Tech-wave bucket by founding year (Dot-Com / Web 2.0 / Mobile & Cloud / AI & Modern) |
| `Legacy_Pre2000` | 1 if founded ≤2000 (non-startup legacy outliers, e.g. Otto Bock 1919); filter these out if desired |
| `Date_Joined`, `Year_Joined` | When the company became a unicorn |
| `Years_to_Unicorn` | Year_Joined − Year_Founded (has extreme outliers for legacy firms) |
| `Valuation_USD`, `Valuation_B` | Valuation in USD and in $B |
| `Valuation_Tier` | Bracket: $1-2B / $2-5B / $5-10B / $10B+ (Decacorn) |
| `Is_Decacorn` | 1 if valuation ≥ $10B |
| `Funding_USD`, `Funding_M` | Total funding raised, in USD and in $M |
| `Capital_Multiple` | Valuation ÷ Funding (valuation created per $ raised); null where funding is 0/missing |
| `Num_Investors` | Count of investors listed in Select_Investors |
| `Select_Investors` | Original comma-separated investor list (kept for reference) |

## Data Dictionary — `unicorns_investors.csv`

| Column | Meaning |
|--------|---------|
| `Company` | Company name (join key to main) |
| `Investor` | A single investor (one per row) |
| `Industry`, `Country`, `Continent` | Denormalized from main for easy investor-by-segment analysis |
| `Valuation_B`, `Year_Joined`, `Is_Decacorn` | Denormalized company attributes |

---

## Suggested Dashboard Tabs

| Tab | Question it answers | Key fields |
|-----|--------------------|-----------|
| **Overview** | The unicorn landscape at a glance | KPIs (count, total/median Valuation_B, median Years_to_Unicorn) + map |
| **Geography** | Where are unicorns created? | Country/City map, Continent filter |
| **Industry** | Which sectors dominate? | Industry counts, Valuation_B & Capital_Multiple by Industry |
| **Trends** | How has it changed over time? | Year_Joined timeline, Founding_Era, sector mix over time |
| **Investors** | Who funds unicorns, and what? | Top Investor by count, Investor × Industry (investors table) |
| **Comps Finder** | "What's a company like this worth?" | Filters: Industry + Continent + Years_to_Unicorn → Valuation_B / Capital_Multiple distribution |

**Tip:** give every view a short "so-what" caption, keep one narrative (e.g. "a VC's field
guide to unicorns"), and note the data caveats below on the Overview tab.

---

## Data Caveats (state these on the dashboard)

- **Snapshot only** (~April 2022): no unicorns added after; companies that later exited or
  fell below $1B are not tracked. Trends reflect *surviving* unicorns.
- **Survivorship**: this is a success-only population, so it describes what unicorns look
  like — not the odds that any given company becomes one.
- **Legacy outliers**: a few pre-2000 firms inflate `Years_to_Unicorn`; use `Legacy_Pre2000`
  to exclude them when needed.
