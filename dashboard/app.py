"""
Unicorn Companies — Interactive Dashboard (Streamlit)
A VC's field guide to unicorns, built on the CB Insights snapshot (~April 2022).

Run:  streamlit run app.py
"""
import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

DIR = os.path.dirname(os.path.abspath(__file__))
ACCENT = "#2563EB"
SEQ = px.colors.sequential.Blues

st.set_page_config(page_title="Unicorn Dashboard", page_icon="🦄", layout="wide")


# ── data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    main = pd.read_csv(os.path.join(DIR, "unicorns_main.csv"))
    inv = pd.read_csv(os.path.join(DIR, "unicorns_investors.csv"))
    main["Date_Joined"] = pd.to_datetime(main["Date_Joined"])
    return main, inv


main, investors = load_data()

# ── header ───────────────────────────────────────────────────────────────────
st.title("🦄 Unicorn Companies — A VC's Field Guide")
st.caption("Interactive analysis of 1,074 unicorns · CB Insights snapshot (~April 2022) · "
           "an *insight* dashboard, not a predictor.")

# ── sidebar filters ──────────────────────────────────────────────────────────
st.sidebar.header("Filters")
continents = st.sidebar.multiselect(
    "Continent", sorted(main["Continent"].dropna().unique()),
    default=sorted(main["Continent"].dropna().unique()))
industries = st.sidebar.multiselect(
    "Industry", sorted(main["Industry"].dropna().unique()), default=[])
tiers = st.sidebar.multiselect(
    "Valuation tier", sorted(main["Valuation_Tier"].dropna().unique()), default=[])
exclude_legacy = st.sidebar.checkbox(
    "Exclude pre-2000 legacy firms", value=True,
    help="Removes non-startup outliers like Otto Bock (founded 1919).")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Data caveats**\n\n"
    "- Snapshot only (~Apr 2022); no later unicorns, exits not tracked.\n"
    "- Success-only population (survivorship): describes what unicorns look like, "
    "not the odds of becoming one.")

# apply filters
df = main.copy()
if continents:
    df = df[df["Continent"].isin(continents)]
if industries:
    df = df[df["Industry"].isin(industries)]
if tiers:
    df = df[df["Valuation_Tier"].isin(tiers)]
if exclude_legacy:
    df = df[df["Legacy_Pre2000"] == 0]

if df.empty:
    st.warning("No companies match the current filters. Loosen them in the sidebar.")
    st.stop()

inv_f = investors[investors["Company"].isin(df["Company"])]


def caption(text):
    st.info(f"**What this shows —** {text}")


# ── tabs ─────────────────────────────────────────────────────────────────────
tab_over, tab_geo, tab_ind, tab_trend, tab_inv, tab_comps = st.tabs(
    ["📊 Overview", "🌍 Geography", "🏭 Industry", "📈 Trends",
     "💼 Investors", "🔍 Comps Finder"])

# ---- Overview ----
with tab_over:
    st.subheader("The unicorn landscape at a glance")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Unicorns", f"{len(df):,}")
    c2.metric("Total value", f"${df['Valuation_B'].sum():,.0f}B")
    c3.metric("Median valuation", f"${df['Valuation_B'].median():.1f}B")
    c4.metric("Median yrs to unicorn", f"{df['Years_to_Unicorn'].median():.0f}")
    c5.metric("Decacorns ($10B+)", f"{int(df['Is_Decacorn'].sum())}")

    colA, colB = st.columns(2)
    with colA:
        tier = df["Valuation_Tier"].value_counts().sort_index()
        fig = px.bar(x=tier.index, y=tier.values, color=tier.index,
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     labels={"x": "Valuation tier", "y": "Companies"})
        fig.update_layout(showlegend=False, height=360, title="By valuation tier")
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        top = df["Industry"].value_counts().head(8).sort_values()
        fig = px.bar(x=top.values, y=top.index, orientation="h",
                     color_discrete_sequence=[ACCENT],
                     labels={"x": "Companies", "y": ""})
        fig.update_layout(height=360, title="Top industries")
        st.plotly_chart(fig, use_container_width=True)
    caption("Most unicorns cluster just above the $1B line ($1-5B); true giants are rare. "
            "Fintech and Internet Software lead the industry mix.")

# ---- Geography ----
with tab_geo:
    st.subheader("Where are unicorns created?")
    by_country = df.groupby("Country").agg(
        Companies=("Company", "count"),
        Median_Val=("Valuation_B", "median")).reset_index()
    fig = px.choropleth(by_country, locations="Country", locationmode="country names",
                        color="Companies", color_continuous_scale=SEQ,
                        hover_data=["Median_Val"])
    fig.update_layout(height=420, title="Unicorns by country",
                      margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        cty = df["Country"].value_counts().head(12).sort_values()
        fig = px.bar(x=cty.values, y=cty.index, orientation="h",
                     color_discrete_sequence=[ACCENT], labels={"x": "Companies", "y": ""})
        fig.update_layout(height=380, title="Top 12 countries")
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        city = df["City"].value_counts().head(12).sort_values()
        fig = px.bar(x=city.values, y=city.index, orientation="h",
                     color_discrete_sequence=["#7C3AED"], labels={"x": "Companies", "y": ""})
        fig.update_layout(height=380, title="Top 12 cities")
        st.plotly_chart(fig, use_container_width=True)
    caption("Unicorns concentrate in a few hubs even more tightly than a few countries — "
            "cities like San Francisco, New York and Beijing dominate.")

# ---- Industry ----
with tab_ind:
    st.subheader("Which sectors dominate — and how efficiently?")
    agg = df.groupby("Industry").agg(
        Companies=("Company", "count"),
        Median_Valuation_B=("Valuation_B", "median"),
        Median_Multiple=("Capital_Multiple", "median")).reset_index()

    colA, colB = st.columns(2)
    with colA:
        d = agg.sort_values("Companies")
        fig = px.bar(d, x="Companies", y="Industry", orientation="h",
                     color_discrete_sequence=[ACCENT])
        fig.update_layout(height=460, title="Number of unicorns")
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        d = agg.dropna(subset=["Median_Multiple"]).sort_values("Median_Multiple")
        fig = px.bar(d, x="Median_Multiple", y="Industry", orientation="h",
                     color="Median_Multiple", color_continuous_scale="RdYlGn",
                     labels={"Median_Multiple": "Valuation / Funding (x)"})
        fig.update_layout(height=460, title="Capital efficiency (median multiple)")
        st.plotly_chart(fig, use_container_width=True)
    caption("Software-type sectors (Internet Software, Fintech) turn each $ raised into ~6x "
            "valuation; asset-heavy sectors (Auto, Travel) only ~3x.")

# ---- Trends ----
with tab_trend:
    st.subheader("How has the unicorn population evolved?")
    by_year = df["Year_Joined"].value_counts().sort_index()
    fig = px.bar(x=by_year.index, y=by_year.values,
                 color_discrete_sequence=[ACCENT],
                 labels={"x": "Year became a unicorn", "y": "Companies"})
    fig.update_layout(height=340, title="Unicorns created per year")
    st.plotly_chart(fig, use_container_width=True)

    era_ind = (df.groupby(["Founding_Era", "Industry"]).size()
               .reset_index(name="n"))
    top6 = df["Industry"].value_counts().head(6).index
    era_ind = era_ind[era_ind["Industry"].isin(top6)]
    fig = px.line(era_ind, x="Founding_Era", y="n", color="Industry", markers=True,
                  labels={"Founding_Era": "Founding era", "n": "Companies"})
    fig.update_layout(height=380, title="Industry mix across founding eras (top 6)")
    st.plotly_chart(fig, use_container_width=True)
    caption("Unicorn creation spiked in 2021. Across founding eras, Internet Software faded "
            "while Fintech and AI rose — though the shift is directional, not dramatic.")

# ---- Investors ----
with tab_inv:
    st.subheader("Who funds unicorns — and what do they back?")
    top_inv = inv_f["Investor"].value_counts().head(15).sort_values()
    fig = px.bar(x=top_inv.values, y=top_inv.index, orientation="h",
                 color_discrete_sequence=[ACCENT], labels={"x": "Unicorns backed", "y": ""})
    fig.update_layout(height=460, title="Top 15 investors by number of unicorns")
    st.plotly_chart(fig, use_container_width=True)

    sel = st.selectbox("Inspect an investor's sector focus",
                       inv_f["Investor"].value_counts().head(30).index)
    sub = inv_f[inv_f["Investor"] == sel]["Industry"].value_counts().sort_values()
    fig = px.bar(x=sub.values, y=sub.index, orientation="h",
                 color_discrete_sequence=["#7C3AED"], labels={"x": "Unicorns", "y": ""})
    fig.update_layout(height=360, title=f"{sel} — unicorns by industry")
    st.plotly_chart(fig, use_container_width=True)
    caption("A small set of funds (Accel, Tiger Global, a16z, Sequoia) recur behind a large "
            "share of unicorns — investor backing is a strong signal.")

# ---- Comps Finder ----
with tab_comps:
    st.subheader("🔍 Comps Finder — benchmark a company against similar unicorns")
    st.write("Pick a profile; see the valuation & multiple range of comparable *successful* "
             "companies. (Remember: this is a unicorn benchmark, i.e. an upper-tier reference.)")

    c1, c2, c3 = st.columns(3)
    with c1:
        f_ind = st.multiselect("Industry", sorted(main["Industry"].unique()),
                               default=["Fintech"])
    with c2:
        f_cont = st.multiselect("Continent", sorted(main["Continent"].dropna().unique()),
                                default=[])
    with c3:
        yr_lo, yr_hi = st.slider("Years to unicorn", 0, 25, (0, 25))

    comps = main.copy()
    if f_ind:
        comps = comps[comps["Industry"].isin(f_ind)]
    if f_cont:
        comps = comps[comps["Continent"].isin(f_cont)]
    comps = comps[(comps["Years_to_Unicorn"] >= yr_lo) &
                  (comps["Years_to_Unicorn"] <= yr_hi)]

    if len(comps) < 3:
        st.warning(f"Only {len(comps)} comparable companies — too few for a reliable "
                   "benchmark. Broaden the profile.")
    else:
        m = comps["Capital_Multiple"].dropna()
        v = comps["Valuation_B"].dropna()
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Comparable companies", len(comps))
        k2.metric("Median valuation", f"${v.median():.1f}B")
        k3.metric("Median multiple", f"{m.median():.1f}x")
        k4.metric("Multiple range (P25-P75)", f"{m.quantile(.25):.1f}-{m.quantile(.75):.1f}x")

        fig = px.histogram(comps, x="Capital_Multiple", nbins=25,
                           color_discrete_sequence=[ACCENT])
        fig.update_layout(height=320, title="Valuation/Funding multiple — comparable unicorns",
                          xaxis_title="Multiple (x)", yaxis_title="Companies")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Comparable companies**")
        st.dataframe(
            comps[["Company", "Industry", "Country", "Year_Founded",
                   "Valuation_B", "Funding_M", "Capital_Multiple"]]
            .sort_values("Valuation_B", ascending=False).reset_index(drop=True),
            use_container_width=True, height=280)
    caption("Instead of a black-box prediction, you see the actual spread of comparable "
            "successful companies — a transparent benchmark a VC can reason about.")
