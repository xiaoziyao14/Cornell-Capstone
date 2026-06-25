# Descriptive Analysis — Unicorn Companies

**Dataset:** `Data/Unicorn_Companies.csv` (the original, definition-compliant dataset)
**Scope:** 1,074 unicorn companies (private, venture-backed startups valued at ≥ $1B)
**Coverage window:** Companies that reached unicorn status between 2007-07-02 and **2022-04-05**

> **Note on the data:** This analysis describes the population of *existing* unicorns only.
> Rates and shares reported here describe the composition of this dataset, not the
> real-world probability that a company becomes a unicorn.

## Deliverables

| File | What it is |
|------|------------|
| **`Unicorn_Descriptive_Analysis_Report.docx`** | **Full Word report** — Section A (guided analysis), Section B (independent insights), Section C (modeling implications), with tables + embedded charts. |
| `unicorn_descriptive.py` | Generates figures 01–08 (guided analysis). |
| `insight_charts.py` | Generates figures 09–11 (independent insights). |
| `build_report.py` | Assembles the Word report from the data + charts. |
| `01–11_*.png` | Individual chart images. |

---

## Data Cleaning Applied

| Issue | Fix |
|-------|-----|
| Industry capitalization inconsistency (`Artificial Intelligence` × 11 vs `Artificial intelligence` × 73) | Merged into a single canonical category → **84 companies (7.8%)** |
| `Valuation` / `Funding` stored as strings (`$180B`, `$8B`) | Parsed into numeric USD (`Valuation_USD`, `Funding_USD`) |
| `Date Joined` stored as text | Parsed to datetime; derived `Year Joined` and `Years_to_Unicorn` |

---

## Key Findings

### 1. Geographic Distribution — `01_geographic_distribution.png`
- **North America dominates (54.8%)**; the United States alone accounts for **52.3%**.
- **Asia is second (28.9%)**, driven by China (16.1%) and India (6.1%).
- Europe contributes 13.3%, spread across the UK, Germany, and France.
- The top three countries — **US, China, India — make up 74.5%** of all unicorns.

### 2. Industry Distribution — `02_industry_distribution.png`
- **Fintech (20.9%)** and **Internet Software & Services (19.1%)** together account for ~40%.
- E-commerce (10.3%), Artificial Intelligence (7.8%), and Health (6.9%) form the second tier.

### 3. Valuation Distribution — `03_valuation_distribution.png`
- Median valuation **$2B**; mean $3.5B, skewed by ByteDance at **$180B**.
- **94.3% of unicorns sit in the $1B–$10B range**; mega-unicorns ($50B+) are rare.
- Shown as valuation brackets so the heavily right-skewed distribution stays readable.

### 4. Funding Distribution — `04_funding_distribution.png`
- Median total funding **$370M**; **65.4% raised under $500M**.
- Funding (cash raised) is much smaller than valuation (market value): roughly a
  **5:1 valuation-to-funding ratio**, reflecting investor growth premiums.
- Shown as funding brackets for the same readability reason as valuation.

### 5. Timeline — `05_timeline.png`
- Most unicorns were **founded after 2010**, peaking in the mid-2010s.
- Unicorn entries surged in **2021 (520 companies)** — a low-rate, capital-rich boom year.

### 6. Time to Unicorn — `06_years_to_unicorn.png`
- Among companies that *did* become unicorns, the median time from founding is **6 years**
  (mean 7 years).
- **Survivorship-bias caveat:** the dataset contains unicorns only, so this chart describes
  the *timing of successes*, not the *odds of success*. It cannot support any claim that
  "taking longer raises the chance of becoming a unicorn" — there is no data on companies
  that never reached $1B.
- Range is wide: some reach $1B the same year; extreme outliers exist (up to 98 years)
  and should be handled before modeling.

### 7. Industry × Continent Heatmap — `07_industry_continent_heatmap.png`
- Internet Software and Health unicorns concentrate heavily in **North America**.
- E-commerce has its strongest presence in **Asia**.
- Fintech is strong across both North America and Europe.

### 8. Technological Eras — `08_technological_eras.png`
Unicorns are grouped by **founding year** into four technology waves, to trace how
each era's dominant technology produced a different mix of breakout companies.

| Era | Founded | Unicorns | Dominant tech wave |
|-----|---------|----------|--------------------|
| Dot-Com & Early Web | ≤2000 | 37 (3.4%) | First commercial internet; mix still led by Health & Fintech (legacy firms) |
| Web 2.0 & Social | 2001–2008 | 109 (10.1%) | Broadband + social media → **Internet Software jumps to 25.7%** |
| Mobile & Cloud | 2009–2014 | 447 (41.6%) | Smartphones, cloud, sharing economy → **AI first appears (8.3%)**, Fintech rises |
| AI & Modern Stack | 2015–2021 | 481 (44.8%) | AI/ML mainstream, modern fintech → **Fintech peaks at 26.2%**, AI sustained |

**Narrative the chart tells:**
- **Internet Software & Services** peaked in the Web 2.0 era (25.7%) and has steadily
  declined since as the web became commoditized.
- **Fintech** rose continuously across every era, becoming the single largest category
  in the modern stack (26.2%) — the defining unicorn engine of the 2010s–2020s.
- **Artificial Intelligence** was effectively absent before 2009, then emerged with the
  Mobile & Cloud era and held a steady ~8–9% share afterward.
- **E-commerce** and **Health** stayed structurally present but never dominant.

*Note:* eras are defined by **founding year** (a structural view of which tech wave
spawned the company), not by the year the company reached $1B.

---

## Independent Data-Driven Insights (Section B)

An unguided scan of the data — including the previously unused `Select Investors` field —
surfaced several non-obvious patterns. Full detail (with charts) is in the Word report.

1. **Capital efficiency varies sharply by industry** (`09_capital_efficiency.png`).
   Overall median valuation/funding is **5.2x**. Software-type sectors are most efficient
   (Internet Software 6.4x, Fintech 6.2x); asset-heavy sectors least (Auto 2.7x, Travel 2.8x).
2. **A small set of investors backs a large share.** Accel (60), Tiger Global (53),
   Andreessen Horowitz (53), and the Sequoia family (~47–48 each) recur across the population.
3. **Unicorns are a city phenomenon** (`10_country_specialization.png` companion).
   Top 3 cities — San Francisco (14.2%), New York (9.6%), Beijing (5.9%) — make up **29.6%**.
4. **Strong national industry specialization.** UK is **60% Fintech**, Israel **30%
   Cybersecurity**, India/China e-commerce-led → Country and Industry are correlated.
5. **Two speed extremes.** 10.5% reached $1B within 2 years (57 in 2021 alone); 21 took
   over 20 years (Otto Bock HealthCare, founded **1919**, is not a true startup).
6. **Funding and valuation are only weakly linked** (`11_funding_vs_valuation.png`).
   Log-log correlation is **0.60** → money raised explains only ~36% of valuation variance.

---

## Limitations for Modeling

1. **Coverage ends April 2022** — no data on unicorns from 2023 onward. For recent-trend
   analysis a newer source (e.g., CB Insights) would be required.
2. **Descriptive only** — this dataset contains unicorns exclusively, so it cannot, on its
   own, support a model that predicts *whether* a company becomes a unicorn. That requires
   a labeled dataset with non-unicorns (see `Data/dataset_clean.csv`).
3. **Outliers** in `Years_to_Unicorn` and right-skewed valuation/funding should be
   transformed or capped before use in distance-based models (e.g., K-means).
4. **Country and Industry are correlated** (national specialization) — avoid treating them
   as independent features.
5. **Capital efficiency** (Valuation/Funding) is a useful engineered feature; **funding
   alone is a weak predictor** of valuation (r ≈ 0.60).

---

## Methodology Note — Why We Did Not Build a Unicorn-vs-Non-Unicorn Classifier
*(internal record; deliberately kept out of the client-facing report)*

The original goal was to predict which non-unicorn companies are most likely to become
unicorns. After inspecting `Data/dataset_clean.csv` we concluded this supervised framing is
not well supported by the available data, for three connected reasons:

1. **Private companies expose little data.** Private firms file no public financials, so the
   features that actually predict success (revenue, growth, margins, headcount) are not
   collectible. Only round-level facts (funding, founding year, location, sector, investors)
   are reliably available — exactly the thin columns we have. Note unicorns are in fact the
   *best*-documented private companies; quietly failed startups leave almost no trace.
2. **Comparable negatives are nearly impossible to assemble.** A fair study needs
   "matched controls" — companies similar in sector, vintage, geography, and funding that did
   *not* become unicorns. These are under-recorded (survivorship/coverage bias in sources like
   Crunchbase). The well-funded "near-miss" companies that would make good controls are almost
   absent from `dataset_clean.csv` (only ~16 non-unicorns raised ≥ $50M).
3. **Mixing the two classes is therefore a biased case-control design.** The groups differ
   even in *which fields are populated* (asymmetric missingness), so a classifier would learn
   data-collection artifacts and selection bias rather than a genuine success signal.

**Decision:** pivot away from mixed-class classification toward analyses grounded in the
clean unicorn data — unicorn-archetype clustering and within-unicorn driver analysis
(valuation / time-to-unicorn). This reasoning is recorded here for the team; it is not
included in the client-facing report.

---

## Reproducing This Analysis

```bash
cd "descriptive analysis"
python3 unicorn_descriptive.py   # figures 01–08 (guided analysis)
python3 insight_charts.py        # figures 09–11 (independent insights)
python3 build_report.py          # assembles the Word report
```

Requires `pandas`, `numpy`, `matplotlib`, `python-docx`.
