"""
visualizations.py
All chart-generation functions used by the Streamlit app.
Each function returns a matplotlib or plotly figure.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Theme ───────────────────────────────────────────────────
PALETTE = {
    'primary': '#1B2838',
    'accent': '#F7B731',
    'accent2': '#E55A3C',
    'accent3': '#2ECC71',
    'accent4': '#3498DB',
    'bg': '#0E1117',
    'card': '#1B2838',
    'text': '#FAFAFA',
    'muted': '#8899AA',
}

CATEGORICAL_COLORS = ['#F7B731', '#E55A3C', '#3498DB', '#2ECC71', '#9B59B6', '#1ABC9C', '#E67E22', '#EC407A']

sns.set_theme(style="dark", rc={
    'figure.facecolor': PALETTE['bg'],
    'axes.facecolor': PALETTE['card'],
    'text.color': PALETTE['text'],
    'axes.labelcolor': PALETTE['text'],
    'xtick.color': PALETTE['muted'],
    'ytick.color': PALETTE['muted'],
    'grid.color': '#2C3E50',
    'axes.edgecolor': '#2C3E50',
})


def _plotly_layout(fig, title="", height=480):
    """Apply consistent dark theme to plotly figures."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=PALETTE['text'])),
        paper_bgcolor=PALETTE['bg'],
        plot_bgcolor=PALETTE['card'],
        font=dict(color=PALETTE['text'], size=12),
        height=height,
        margin=dict(l=60, r=30, t=60, b=50),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=PALETTE['muted'])),
    )
    fig.update_xaxes(gridcolor='#2C3E50', zerolinecolor='#2C3E50')
    fig.update_yaxes(gridcolor='#2C3E50', zerolinecolor='#2C3E50')
    return fig


# ══════════════════════════════════════════════════════════════
# SECTION 1: DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════

def plot_age_distribution(df):
    order = ['18-24', '25-34', '35-44', '45-54', '55-65']
    counts = df['Q1_Age_Group'].value_counts().reindex(order)
    fig = go.Figure(go.Bar(
        x=counts.index, y=counts.values,
        marker_color=PALETTE['accent'],
        text=counts.values, textposition='outside',
        textfont=dict(color=PALETTE['text'])
    ))
    return _plotly_layout(fig, "Age Group Distribution")


def plot_gender_split(df):
    counts = df['Q2_Gender'].value_counts()
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values,
        hole=0.45,
        marker=dict(colors=CATEGORICAL_COLORS[:len(counts)]),
        textinfo='label+percent',
        textfont=dict(size=13)
    ))
    return _plotly_layout(fig, "Gender Distribution", height=400)


def plot_nationality_distribution(df):
    counts = df['Q3_Nationality_Cluster'].value_counts()
    fig = go.Figure(go.Bar(
        y=counts.index, x=counts.values,
        orientation='h',
        marker_color=CATEGORICAL_COLORS[:len(counts)],
        text=counts.values, textposition='outside',
        textfont=dict(color=PALETTE['text'])
    ))
    return _plotly_layout(fig, "Nationality Cluster Distribution")


def plot_income_distribution(df):
    order = ['Below 3,000', '3,000-10,000', '10,001-20,000', '20,001-35,000', '35,001-50,000', 'Above 50,000']
    counts = df['Q4_Monthly_Income'].value_counts().reindex(order).fillna(0)
    fig = go.Figure(go.Bar(
        x=counts.index, y=counts.values,
        marker_color=PALETTE['accent4'],
        text=counts.values.astype(int), textposition='outside',
        textfont=dict(color=PALETTE['text'])
    ))
    fig.update_xaxes(tickangle=30)
    return _plotly_layout(fig, "Monthly Income Distribution (USD)")


# ══════════════════════════════════════════════════════════════
# SECTION 2: FAN PROFILE & PREFERENCES
# ══════════════════════════════════════════════════════════════

def plot_sport_by_nationality(df):
    ct = pd.crosstab(df['Q3_Nationality_Cluster'], df['Q5_Favorite_Sport'], normalize='index') * 100
    fig = go.Figure()
    for i, sport in enumerate(ct.columns):
        fig.add_trace(go.Bar(
            name=sport, y=ct.index, x=ct[sport],
            orientation='h',
            marker_color=CATEGORICAL_COLORS[i % len(CATEGORICAL_COLORS)]
        ))
    fig.update_layout(barmode='stack')
    return _plotly_layout(fig, "Favorite Sport by Nationality (%)", height=500)


def plot_fan_type_by_age(df):
    ct = pd.crosstab(df['Q1_Age_Group'], df['Q7_Fan_Type'], normalize='index') * 100
    order = ['18-24', '25-34', '35-44', '45-54', '55-65']
    ct = ct.reindex(order)
    fan_order = ['Casual viewer', 'Passionate fan', 'Hardcore collector', 'Investment buyer']
    fig = go.Figure()
    for i, fan in enumerate(fan_order):
        if fan in ct.columns:
            fig.add_trace(go.Bar(
                name=fan, x=ct.index, y=ct[fan],
                marker_color=CATEGORICAL_COLORS[i]
            ))
    fig.update_layout(barmode='stack')
    return _plotly_layout(fig, "Fan Type Composition by Age Group (%)")


def plot_jersey_type_by_fan(df):
    ct = pd.crosstab(df['Q7_Fan_Type'], df['Q10_Jersey_Type_Interest'], normalize='index') * 100
    fig = px.imshow(
        ct.values,
        x=ct.columns.tolist(), y=ct.index.tolist(),
        color_continuous_scale='YlOrRd',
        text_auto='.1f',
        labels=dict(color='%')
    )
    return _plotly_layout(fig, "Jersey Type Interest by Fan Type (Heatmap %)", height=420)


def plot_authentication_by_fan(df):
    fan_order = ['Casual viewer', 'Passionate fan', 'Hardcore collector', 'Investment buyer']
    fig = go.Figure()
    for i, fan in enumerate(fan_order):
        subset = df[df['Q7_Fan_Type'] == fan]['Q11_Authentication_Importance']
        fig.add_trace(go.Box(
            y=subset, name=fan,
            marker_color=CATEGORICAL_COLORS[i],
            boxmean=True
        ))
    return _plotly_layout(fig, "Authentication Importance by Fan Type (1–5)")


def plot_rarity_by_fan(df):
    fan_order = ['Casual viewer', 'Passionate fan', 'Hardcore collector', 'Investment buyer']
    fig = go.Figure()
    for i, fan in enumerate(fan_order):
        subset = df[df['Q7_Fan_Type'] == fan]['Q14_Rarity_Importance']
        fig.add_trace(go.Box(
            y=subset, name=fan,
            marker_color=CATEGORICAL_COLORS[i],
            boxmean=True
        ))
    return _plotly_layout(fig, "Rarity Importance by Fan Type (1–5)")


def plot_vintage_interest(df):
    ct = pd.crosstab(df['Q7_Fan_Type'], df['Q15_Vintage_Interest'], normalize='index') * 100
    vintage_order = ['Yes, very interested', 'Somewhat interested', 'Not interested']
    fig = go.Figure()
    for i, cat in enumerate(vintage_order):
        if cat in ct.columns:
            fig.add_trace(go.Bar(
                name=cat, x=ct.index, y=ct[cat],
                marker_color=CATEGORICAL_COLORS[i]
            ))
    fig.update_layout(barmode='group')
    return _plotly_layout(fig, "Vintage Jersey Interest by Fan Type (%)")


# ══════════════════════════════════════════════════════════════
# SECTION 3: PURCHASING BEHAVIOR
# ══════════════════════════════════════════════════════════════

def plot_spend_by_income(df):
    spend_order = ['Under 50', '50-200', '201-500', '501-1,500', '1,501-3,000', '3,000+']
    income_order = ['Below 3,000', '3,000-10,000', '10,001-20,000', '20,001-35,000', '35,001-50,000', 'Above 50,000']
    ct = pd.crosstab(df['Q4_Monthly_Income'], df['Q16_Willingness_to_Spend'], normalize='index') * 100
    ct = ct.reindex(index=income_order, columns=spend_order).fillna(0)
    fig = px.imshow(
        ct.values,
        x=ct.columns.tolist(), y=ct.index.tolist(),
        color_continuous_scale='Viridis',
        text_auto='.0f',
        labels=dict(color='%')
    )
    return _plotly_layout(fig, "Spending Willingness by Income Bracket (%)", height=450)


def plot_spend_by_fan_type(df):
    spend_order = ['Under 50', '50-200', '201-500', '501-1,500', '1,501-3,000', '3,000+']
    ct = pd.crosstab(df['Q7_Fan_Type'], df['Q16_Willingness_to_Spend'], normalize='index') * 100
    ct = ct.reindex(columns=spend_order).fillna(0)
    fig = go.Figure()
    for i, spend in enumerate(spend_order):
        fig.add_trace(go.Bar(
            name=spend, x=ct.index, y=ct[spend],
            marker_color=CATEGORICAL_COLORS[i % len(CATEGORICAL_COLORS)]
        ))
    fig.update_layout(barmode='stack')
    return _plotly_layout(fig, "Spending Willingness by Fan Type (%)")


def plot_discount_influence(df):
    ct = pd.crosstab(df['Q7_Fan_Type'], df['Q18_Discount_Influence'], normalize='index') * 100
    disc_order = ['Strongly influences', 'Somewhat influences', 'No impact']
    colors = [PALETTE['accent'], PALETTE['accent4'], PALETTE['muted']]
    fig = go.Figure()
    for i, d in enumerate(disc_order):
        if d in ct.columns:
            fig.add_trace(go.Bar(
                name=d, x=ct.index, y=ct[d],
                marker_color=colors[i]
            ))
    fig.update_layout(barmode='group')
    return _plotly_layout(fig, "Discount Influence by Fan Type (%)")


def plot_recommendation_by_age(df):
    age_order = ['18-24', '25-34', '35-44', '45-54', '55-65']
    ct = pd.crosstab(df['Q1_Age_Group'], df['Q19_Recommendation_Influence'], normalize='index') * 100
    ct = ct.reindex(age_order)
    rec_order = ['Yes, definitely', 'Maybe', 'No, I prefer browsing on my own']
    colors = [PALETTE['accent3'], PALETTE['accent4'], PALETTE['muted']]
    fig = go.Figure()
    for i, r in enumerate(rec_order):
        if r in ct.columns:
            fig.add_trace(go.Bar(
                name=r, x=ct.index, y=ct[r],
                marker_color=colors[i]
            ))
    fig.update_layout(barmode='group')
    return _plotly_layout(fig, "AI Recommendation Receptivity by Age (%)")


def plot_frequency_by_fan(df):
    freq_order = ['Once a year or less', '2-4 times a year', '5-10 times a year', 'More than 10 times a year']
    ct = pd.crosstab(df['Q7_Fan_Type'], df['Q17_Purchase_Frequency'], normalize='index') * 100
    ct = ct.reindex(columns=freq_order).fillna(0)
    fig = go.Figure()
    for i, f in enumerate(freq_order):
        fig.add_trace(go.Bar(
            name=f, x=ct.index, y=ct[f],
            marker_color=CATEGORICAL_COLORS[i]
        ))
    fig.update_layout(barmode='stack')
    return _plotly_layout(fig, "Purchase Frequency by Fan Type (%)")


# ══════════════════════════════════════════════════════════════
# SECTION 4: PLATFORM VALIDATION
# ══════════════════════════════════════════════════════════════

def plot_platform_adoption(df):
    order = ['Definitely yes', 'Probably yes', 'Not sure', 'Probably no', 'Definitely no']
    counts = df['Q21_Would_Use_Platform'].value_counts().reindex(order)
    colors = [PALETTE['accent3'], '#27AE60', PALETTE['accent4'], PALETTE['accent2'], '#C0392B']
    fig = go.Figure(go.Bar(
        x=counts.index, y=counts.values,
        marker_color=colors,
        text=counts.values, textposition='outside',
        textfont=dict(color=PALETTE['text'])
    ))
    return _plotly_layout(fig, "Would You Use This Platform?")


def plot_adoption_by_fan(df):
    ct = pd.crosstab(df['Q7_Fan_Type'], df['Q21_Would_Use_Platform'], normalize='index') * 100
    order = ['Definitely yes', 'Probably yes', 'Not sure', 'Probably no', 'Definitely no']
    ct = ct.reindex(columns=order).fillna(0)
    colors = ['#2ECC71', '#27AE60', '#3498DB', '#E55A3C', '#C0392B']
    fig = go.Figure()
    for i, col in enumerate(order):
        fig.add_trace(go.Bar(
            name=col, x=ct.index, y=ct[col],
            marker_color=colors[i]
        ))
    fig.update_layout(barmode='stack')
    return _plotly_layout(fig, "Platform Adoption by Fan Type (%)")


def plot_trust_factors(df):
    trust_cols = {
        'Trust_Third-party': 'Third-party Auth',
        'Trust_Blockchain': 'Blockchain',
        'Trust_Seller': 'Seller Ratings',
        'Trust_Money-back': 'Money-back Guarantee',
        'Trust_AI-powered': 'AI Authenticity'
    }
    counts = {}
    for col, label in trust_cols.items():
        if col in df.columns:
            counts[label] = df[col].sum()
    counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    fig = go.Figure(go.Bar(
        y=list(counts.keys()), x=list(counts.values()),
        orientation='h',
        marker_color=CATEGORICAL_COLORS[:len(counts)],
        text=list(counts.values()), textposition='outside',
        textfont=dict(color=PALETTE['text'])
    ))
    return _plotly_layout(fig, "Trust Factors — What Builds Confidence?")


def plot_resell_interest(df):
    ct = pd.crosstab(df['Q7_Fan_Type'], df['Q23_Would_Resell'], normalize='index') * 100
    resell_order = ['Yes', 'Maybe', 'No']
    colors = [PALETTE['accent3'], PALETTE['accent'], PALETTE['accent2']]
    fig = go.Figure()
    for i, r in enumerate(resell_order):
        if r in ct.columns:
            fig.add_trace(go.Bar(
                name=r, x=ct.index, y=ct[r],
                marker_color=colors[i]
            ))
    fig.update_layout(barmode='group')
    return _plotly_layout(fig, "Reselling Interest by Fan Type (%)")


def plot_top_feature_ranked(df):
    counts = df[df['Top_Feature'] != 'Not provided']['Top_Feature'].value_counts()
    fig = go.Figure(go.Bar(
        x=counts.values, y=counts.index,
        orientation='h',
        marker_color=[PALETTE['accent'], PALETTE['accent2'], PALETTE['accent4'], PALETTE['accent3']],
        text=counts.values, textposition='outside',
        textfont=dict(color=PALETTE['text'])
    ))
    return _plotly_layout(fig, "Most Important Feature (#1 Ranked)")


def plot_loyalty_interest(df):
    counts = df['Q24_Loyalty_Interest'].value_counts()
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values,
        hole=0.45,
        marker=dict(colors=[PALETTE['accent3'], PALETTE['accent'], PALETTE['muted']]),
        textinfo='label+percent',
        textfont=dict(size=13)
    ))
    return _plotly_layout(fig, "Loyalty Program Interest", height=400)


# ══════════════════════════════════════════════════════════════
# SECTION 5: CORRELATION & ADVANCED
# ══════════════════════════════════════════════════════════════

def plot_correlation_heatmap(df):
    numeric_cols = [
        'Age_Numeric', 'Income_Numeric', 'Q11_Authentication_Importance',
        'Q13_Player_Popularity_Importance', 'Q14_Rarity_Importance',
        'Spend_Numeric', 'Freq_Numeric', 'Collector_Score',
        'Value_Sensitivity', 'Platform_Adoption'
    ]
    available = [c for c in numeric_cols if c in df.columns]
    corr = df[available].corr()
    labels = [c.replace('_', ' ').replace('Q11 ', '').replace('Q13 ', '').replace('Q14 ', '') for c in available]
    fig = px.imshow(
        corr.values,
        x=labels, y=labels,
        color_continuous_scale='RdYlBu_r',
        text_auto='.2f',
        zmin=-1, zmax=1
    )
    return _plotly_layout(fig, "Correlation Heatmap — Key Variables", height=560)


def plot_collector_score_distribution(df):
    fig = go.Figure()
    fan_types = ['Casual viewer', 'Passionate fan', 'Hardcore collector', 'Investment buyer']
    for i, ft in enumerate(fan_types):
        subset = df[df['Q7_Fan_Type'] == ft]['Collector_Score']
        fig.add_trace(go.Histogram(
            x=subset, name=ft,
            marker_color=CATEGORICAL_COLORS[i],
            opacity=0.7
        ))
    fig.update_layout(barmode='overlay')
    return _plotly_layout(fig, "Collector Score Distribution by Fan Type")


def plot_spend_vs_income_scatter(df):
    df_plot = df.dropna(subset=['Income_Numeric', 'Spend_Numeric']).copy()
    # Add jitter
    df_plot['Income_Jittered'] = df_plot['Income_Numeric'] + np.random.normal(0, 500, len(df_plot))
    df_plot['Spend_Jittered'] = df_plot['Spend_Numeric'] + np.random.normal(0, 30, len(df_plot))
    fig = px.scatter(
        df_plot, x='Income_Jittered', y='Spend_Jittered',
        color='Q7_Fan_Type',
        color_discrete_sequence=CATEGORICAL_COLORS,
        opacity=0.5,
        labels={'Income_Jittered': 'Monthly Income (USD)', 'Spend_Jittered': 'Willing to Spend (USD)'}
    )
    return _plotly_layout(fig, "Income vs Spending Willingness (by Fan Type)", height=500)


def get_key_metrics(df):
    """Return dict of headline KPIs for the dashboard."""
    total = len(df)
    adoption_rate = df['Platform_Adoption'].mean() * 100
    avg_auth = df['Q11_Authentication_Importance'].mean()
    avg_rarity = df['Q14_Rarity_Importance'].mean()
    hardcore_pct = (df['Q7_Fan_Type'].isin(['Hardcore collector', 'Investment buyer'])).mean() * 100
    own_jersey_pct = (df['Q8_Own_Jerseys'] == 'Yes').mean() * 100
    resell_yes = (df['Q23_Would_Resell'] == 'Yes').mean() * 100
    outliers = df['Outlier_Flag'].sum()

    return {
        'total_responses': total,
        'adoption_rate': round(adoption_rate, 1),
        'avg_auth_importance': round(avg_auth, 2),
        'avg_rarity_importance': round(avg_rarity, 2),
        'high_value_segment_pct': round(hardcore_pct, 1),
        'own_jersey_pct': round(own_jersey_pct, 1),
        'resell_interest_pct': round(resell_yes, 1),
        'outlier_count': outliers,
    }
