"""
app.py — Jersey Marketplace Analytics Dashboard
Streamlit dashboard for survey data analysis.
"""

import streamlit as st
import pandas as pd
from data_cleaning import load_and_clean
from visualizations import *

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Jersey Marketplace Analytics",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=DM+Sans:wght@400;500&display=swap');

    .block-container { padding-top: 1.5rem; }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }

    .metric-card {
        background: linear-gradient(135deg, #1B2838 0%, #2C3E50 100%);
        border: 1px solid #3498DB33;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        color: #F7B731;
    }
    .metric-card .metric-label {
        font-size: 0.85rem;
        color: #8899AA;
        margin-top: 4px;
        font-family: 'DM Sans', sans-serif;
    }

    .insight-box {
        background: #1B283844;
        border-left: 4px solid #F7B731;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.8rem 0;
        font-family: 'DM Sans', sans-serif;
        color: #CCDDEE;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #3498DB55, transparent);
        margin: 2rem 0;
    }

    div[data-testid="stExpander"] details summary p {
        font-size: 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ── Load & Clean Data ───────────────────────────────────────
@st.cache_data
def get_data():
    return load_and_clean("data_raw.csv")

df, cleaning_log = get_data()
metrics = get_key_metrics(df)


# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏆 Dashboard Controls")
    st.markdown("---")

    # Filters
    fan_filter = st.multiselect(
        "Filter by Fan Type",
        options=df['Q7_Fan_Type'].unique().tolist(),
        default=df['Q7_Fan_Type'].unique().tolist()
    )
    nat_filter = st.multiselect(
        "Filter by Nationality",
        options=sorted(df['Q3_Nationality_Cluster'].unique().tolist()),
        default=sorted(df['Q3_Nationality_Cluster'].unique().tolist())
    )
    exclude_outliers = st.checkbox("Exclude flagged outliers", value=False)

    st.markdown("---")
    st.markdown("##### Data Cleaning Log")
    with st.expander("View cleaning steps"):
        for step in cleaning_log:
            st.text(step)

    st.markdown("---")
    st.caption("DAIDM Project · SP Jain GMBA · 2025")

# Apply filters
df_filtered = df[
    (df['Q7_Fan_Type'].isin(fan_filter)) &
    (df['Q3_Nationality_Cluster'].isin(nat_filter))
].copy()

if exclude_outliers:
    df_filtered = df_filtered[df_filtered['Outlier_Flag'] == 0]


# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("# 🏆 Rare Jersey Marketplace — Survey Analytics")
st.markdown("*Validating demand for a digital marketplace for rare, game-worn, and collectible sports jerseys*")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── KPI Cards ───────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(df_filtered):,}</div>
        <div class="metric-label">Survey Responses</div>
    </div>""", unsafe_allow_html=True)

with k2:
    adoption = df_filtered['Platform_Adoption'].mean() * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{adoption:.1f}%</div>
        <div class="metric-label">Platform Adoption Rate</div>
    </div>""", unsafe_allow_html=True)

with k3:
    hv = df_filtered['Q7_Fan_Type'].isin(['Hardcore collector', 'Investment buyer']).mean() * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{hv:.1f}%</div>
        <div class="metric-label">High-Value Segments</div>
    </div>""", unsafe_allow_html=True)

with k4:
    own = (df_filtered['Q8_Own_Jerseys'] == 'Yes').mean() * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{own:.1f}%</div>
        <div class="metric-label">Already Own Jerseys</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")


# ══════════════════════════════════════════════════════════════
# TAB LAYOUT
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Demographics",
    "🏅 Fan Profile",
    "💰 Purchase Behavior",
    "🚀 Platform Validation",
    "🔬 Correlations & Insights"
])


# ── TAB 1: Demographics ────────────────────────────────────
with tab1:
    st.markdown("### Respondent Demographics")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_age_distribution(df_filtered), use_container_width=True)
    with c2:
        st.plotly_chart(plot_gender_split(df_filtered), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(plot_nationality_distribution(df_filtered), use_container_width=True)
    with c4:
        st.plotly_chart(plot_income_distribution(df_filtered), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <strong>📌 Insight:</strong> The respondent base skews young (60%+ under 35) and male (68%), consistent
        with sports memorabilia demographics. The UAE-centric nationality mix (South Asian 30%, Arab 25%,
        Western Expat 20%) reflects the target market. Income distribution peaks in the 3K–20K range,
        suggesting mid-market pricing will capture the largest audience.
    </div>""", unsafe_allow_html=True)


# ── TAB 2: Fan Profile ─────────────────────────────────────
with tab2:
    st.markdown("### Fan Profile & Jersey Preferences")

    st.plotly_chart(plot_fan_type_by_age(df_filtered), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_sport_by_nationality(df_filtered), use_container_width=True)
    with c2:
        st.plotly_chart(plot_jersey_type_by_fan(df_filtered), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(plot_authentication_by_fan(df_filtered), use_container_width=True)
    with c4:
        st.plotly_chart(plot_rarity_by_fan(df_filtered), use_container_width=True)

    st.plotly_chart(plot_vintage_interest(df_filtered), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <strong>📌 Insight:</strong> Hardcore collectors and investment buyers rate authentication (avg 4.3/5)
        and rarity (avg 4.5/5) significantly higher than casual viewers. Game-worn jerseys dominate
        interest among collectors/investors, while casuals prefer regular replicas. This validates
        authentication verification as a core platform feature. Vintage interest is strong among
        collectors (55% very interested), suggesting a dedicated vintage section would drive engagement.
    </div>""", unsafe_allow_html=True)


# ── TAB 3: Purchase Behavior ───────────────────────────────
with tab3:
    st.markdown("### Purchasing Behavior & Price Sensitivity")

    st.plotly_chart(plot_spend_by_income(df_filtered), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_spend_by_fan_type(df_filtered), use_container_width=True)
    with c2:
        st.plotly_chart(plot_frequency_by_fan(df_filtered), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(plot_discount_influence(df_filtered), use_container_width=True)
    with c4:
        st.plotly_chart(plot_recommendation_by_age(df_filtered), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <strong>📌 Insight:</strong> Spending scales with income as expected, but fan type is the stronger
        predictor — investment buyers earning 20K+ are willing to spend $1,500–$3,000+ per jersey.
        Discounts strongly influence casual viewers (55%) but have no impact on 55% of investors,
        confirming that dynamic pricing should segment by user type, not apply blanket discounts.
        AI recommendations resonate most with under-35 users (40% definite yes), validating
        the recommendation engine for the platform's core demographic.
    </div>""", unsafe_allow_html=True)


# ── TAB 4: Platform Validation ─────────────────────────────
with tab4:
    st.markdown("### Platform Demand Validation")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_platform_adoption(df_filtered), use_container_width=True)
    with c2:
        st.plotly_chart(plot_adoption_by_fan(df_filtered), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(plot_trust_factors(df_filtered), use_container_width=True)
    with c4:
        st.plotly_chart(plot_top_feature_ranked(df_filtered), use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(plot_resell_interest(df_filtered), use_container_width=True)
    with c6:
        st.plotly_chart(plot_loyalty_interest(df_filtered), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <strong>📌 Insight:</strong> ~56% of respondents would definitely or probably use the platform —
        strong validation signal. Among hardcore collectors and investors, adoption exceeds 75%.
        Authentication verification is the #1 ranked feature across all segments. Third-party
        authentication certificates and seller ratings are the top trust builders. 75% of investment
        buyers would resell on the platform, confirming two-sided marketplace viability.
        Loyalty programs attract 80% interest (strong + somewhat), supporting a points/early-access model.
    </div>""", unsafe_allow_html=True)


# ── TAB 5: Correlations ────────────────────────────────────
with tab5:
    st.markdown("### Correlation Analysis & Advanced Views")

    st.plotly_chart(plot_correlation_heatmap(df_filtered), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_collector_score_distribution(df_filtered), use_container_width=True)
    with c2:
        st.plotly_chart(plot_spend_vs_income_scatter(df_filtered), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <strong>📌 Insight:</strong> The Collector Score (purchase frequency × fan type weight) shows
        clear separation between segments — hardcore collectors cluster at 20–48, while casuals
        sit at 1–3. Platform Adoption correlates most strongly with Collector Score (r ≈ 0.4+)
        and authentication importance, confirming that serious collectors are the primary
        target acquisition segment. Income correlates with spending willingness but not with
        platform adoption, meaning the value proposition resonates across income levels.
    </div>""", unsafe_allow_html=True)

    # Data download
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### 📥 Download Data")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Download Cleaned Dataset (CSV)",
            df.to_csv(index=False).encode('utf-8'),
            "jersey_survey_cleaned.csv",
            "text/csv"
        )
    with c2:
        st.download_button(
            "Download Filtered Dataset (CSV)",
            df_filtered.to_csv(index=False).encode('utf-8'),
            "jersey_survey_filtered.csv",
            "text/csv"
        )
