import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data_processing import get_all_metrics

# --- Configuration & Styling ---
st.set_page_config(page_title="Wayne Enterprises Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Playfair+Display:wght@400;600;700;900&display=swap" rel="stylesheet"><style>
    html, body, [class*="css"] { font-family: 'Playfair Display', serif !important; background-color: #FAFAFA !important; color: #1e293b !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Playfair Display', serif !important; color: #0f172a !important; font-weight: 700 !important; }
    header {visibility: hidden;}
    [data-testid="stSidebar"] { display: none; }
    
    .metric-card { background: #FFFFFF; border-radius: 12px; padding: 24px; text-align: left; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.04); }
    .metric-title { font-size: 1.05rem; color: #64748b; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; }
    .metric-value { font-size: 2.6rem; font-weight: 700; color: #0f172a; margin: 0; }
    
    /* Highlighted Tab Navigation Bar */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 16px; 
        justify-content: center; 
        margin-top: 50px; 
        margin-bottom: 40px; 
        background-color: #f1f5f9; 
        padding: 18px; 
        border-radius: 16px; 
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    .stTabs [data-baseweb="tab"] { 
        background-color: transparent !important; 
        border-radius: 12px !important; 
        padding: 15px 45px; 
        transition: all 0.3s ease-in-out;
        height: auto;
        border: none !important;
        outline: none !important;
    }
    .stTabs [data-baseweb="tab"]:focus,
    .stTabs [data-baseweb="tab"]:active {
        background-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab"] p {
        font-weight: 800 !important; 
        font-size: 1.8rem !important; 
        color: #64748b !important; 
        margin: 0;
        transition: color 0.3s ease-in-out;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { 
        background-color: #0f172a !important; 
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.4) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    .stTabs [data-baseweb="tab"][aria-selected="true"] span {
        color: #FFFFFF !important; 
    }
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover p {
        color: #0f172a !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
        background-color: transparent !important;
    }

    /* Newspaper specific CSS for the analysis section */
    .newspaper-sub-header {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 300;
        letter-spacing: 5px;
        margin-top: 15px;
        text-transform: uppercase;
        border-bottom: 2px solid #111;
        border-top: 1px solid #111;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    .in-charts-badge {
        background-color: #be1e2d;
        color: white;
        padding: 4px 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 1.5rem;
        display: inline-block;
        margin-right: 15px;
        vertical-align: middle;
        letter-spacing: 1px;
    }
    .deep-dive-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 2.2rem;
        text-transform: uppercase;
        vertical-align: middle;
        display: inline-block;
        letter-spacing: 1px;
    }
    .intro-paragraph {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        max-width: 900px;
        margin: 20px auto 30px auto;
        line-height: 1.6;
        color: #333;
    }
    .intro-paragraph b {
        font-weight: 900;
        color: #111;
    }
    
    .story-headline {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        line-height: 1.1;
        margin-bottom: 5px;
        color: #111;
        font-weight: 400;
    }
    .story-category {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #be1e2d;
        text-transform: uppercase;
        font-weight: 900;
        margin-bottom: 2px;
        letter-spacing: 1px;
    }
    .newspaper-text {
        font-family: 'Playfair Display', serif;
        font-size: 1.15rem;
        line-height: 1.5;
        text-align: justify;
        margin-top: 15px;
        color: #222;
    }
    .newspaper-text strong.lead-in {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 1.15rem;
        text-transform: uppercase;
    }
    .newspaper-text strong.intervention {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        color: #be1e2d;
        text-transform: uppercase;
        display: block;
        margin-top: 15px;
        border-top: 1px dashed #ccc;
        padding-top: 8px;
    }
    .chart-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #555;
        font-weight: 600;
        margin-bottom: -10px;
        z-index: 10;
        position: relative;
    }
    
    .horizontal-rule {
        border-top: 1px solid #ccc;
        margin: 40px 0;
    }
    .vertical-rule {
        border-right: 1px solid #ccc;
        height: 100%;
        padding-right: 20px;
    }
    .col-padding-left {
        padding-left: 20px;
    }
    
    .big-number {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 7rem;
        color: #be1e2d;
        line-height: 1;
        text-align: center;
        margin: 40px 0 20px 0;
        letter-spacing: -2px;
    }
    .big-number-sub {
        font-size: 3.5rem;
    }
    </style>""", unsafe_allow_html=True)

# Custom Metric Component
def editorial_metric(title, value):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# Helper for Print-Style Plotly Theme
def apply_plotly_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=11, color="#333"),
        title=None, # We use custom headlines
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=11)),
        margin=dict(l=10, r=10, t=20, b=20),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Inter"),
        xaxis=dict(automargin=True, title_font=dict(size=12), showgrid=True, gridwidth=1, gridcolor='#e5e7eb', zeroline=False),
        yaxis=dict(automargin=True, title_font=dict(size=12), showgrid=True, gridwidth=1, gridcolor='#e5e7eb', zeroline=False)
    )
    fig.layout.title.text = ""
    return fig

def render_headline(headline, category=None):
    cat_html = f'<div class="story-category">{category}</div>' if category else ''
    st.markdown(f"""
        {cat_html}
        <div class="story-headline">{headline}</div>
    """, unsafe_allow_html=True)

def render_chart_subtitle(subtitle):
    st.markdown(f'<div class="chart-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def render_story_text(insight, intervention_text=None):
    words = insight.split()
    if len(words) > 2:
        lead_in = " ".join(words[:2]).upper()
        rest = " ".join(words[2:])
        insight_html = f'<strong class="lead-in">{lead_in}</strong> {rest}'
    else:
        insight_html = insight

    intervention_html = f'<strong class="intervention">Strategic Intervention:</strong> {intervention_text}' if intervention_text else ''
    
    st.markdown(f"""
        <div class="newspaper-text">
            {insight_html}
            {intervention_html}
        </div>
    """, unsafe_allow_html=True)

def render_big_number(number, subtitle=""):
    st.markdown(f'<div class="big-number">{number}<span class="big-number-sub">{subtitle}</span></div>', unsafe_allow_html=True)


# --- Data Loading ---
@st.cache_data
def load_and_process_data():
    return get_all_metrics()

try:
    with st.spinner("Loading Wayne Analytics Engine..."):
        data, p1, p2, p3 = load_and_process_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

VIBRANT_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4']
MINT_COLORS = ['#274e13', '#6aa84f', '#bf9000', '#cc0000', '#0b5394', '#674ea7']

# ==========================================
# REPORT HEADER (ORIGINAL WAYNE STYLE)
# ==========================================
st.markdown("<div style='display: flex; justify-content: center; align-items: center; margin-top: 20px;'><div style='background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; width: 75px; height: 75px; display: flex; justify-content: center; align-items: center; border-radius: 16px; margin-right: 24px; font-family: \"Playfair Display\", serif; font-size: 3.8rem; font-weight: 800; box-shadow: 0 6px 12px rgba(0,0,0,0.15); line-height: 1;'>W</div><h1 style='color: #0f172a; font-size: 4.0rem; margin: 0;'>Wayne Enterprises</h1></div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.4rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 50px;'>Executive Analytics & Strategic Interventions Report</p>", unsafe_allow_html=True)

# ==========================================
# EXECUTIVE OVERVIEW (Always Visible)
# ==========================================
esg = p3['esg']
col1, col2, col3, col4 = st.columns(4)
with col1: editorial_metric("Composite ESG Score", f"{esg['Composite_ESG']:.1f}")
with col2: editorial_metric("Carbon Footprint", f"{esg['Carbon_Footprint']:.0f} MT")
with col3: editorial_metric("Diversity Index", f"{esg['Diversity_Index']:.2f}")
with col4: editorial_metric("Community Events", f"{esg['Community_Events']:.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# TABS NAVIGATION
# ==========================================
tab_diag, tab_pred, tab_strat = st.tabs(["Diagnostics", "Predictive Analytics", "Strategy"])

# --- TAB 1: Diagnostics ---
with tab_diag:
    st.markdown('<div class="newspaper-sub-header">PLAIN FACTS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <span class="in-charts-badge">IN CHARTS</span>
        <span class="deep-dive-title">DIAGNOSTICS DEEP DIVE</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr class='horizontal-rule'>", unsafe_allow_html=True)
    
    # ROW 1: Financial Trajectory & Innovation Economics
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="vertical-rule">', unsafe_allow_html=True)
        render_headline("Broad-Based Uptick", "Financial Trajectory")
        render_chart_subtitle("Revenue by Division Over Time ($M)")
        df_fin = data['finance']
        fig_fin = px.area(df_fin, x=df_fin.index, y='Revenue_M', color='Division', color_discrete_sequence=MINT_COLORS)
        fig_fin.update_traces(line=dict(width=2))
        st.plotly_chart(apply_plotly_theme(fig_fin), use_container_width=True)
        render_story_text(
            "REVENUE CONTINUES its upward trajectory across all major divisions. Our financial data reveals sustained, compounding growth, particularly within Wayne Aerospace and Construction. Historical trends demonstrate high resilience to broader economic downturns, driven by our diversified portfolio.",
            "Maintain aggressive capital deployment in Aerospace. Evaluate Wayne Foundation's cash burn rate to ensure sustainability without compromising our philanthropic mission."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="col-padding-left">', unsafe_allow_html=True)
        render_headline("Growth Gaps", "Innovation Economics")
        render_chart_subtitle("Correlation Strength by Lag Time")
        rd_rev = p1['rd_rev_corr']
        df_corr = pd.DataFrame(rd_rev, index=['0 Lag', '1 Qtr Lag', '2 Qtr Lag']).T
        fig_rd = px.bar(df_corr, barmode='group', color_discrete_sequence=['#9ca3af', '#6b7280', '#1f2937'])
        st.plotly_chart(apply_plotly_theme(fig_rd), use_container_width=True)
        render_story_text(
            "R&D INVESTMENT yields maximum revenue impact after two quarters. By analyzing time-lagged cross-correlations, we discovered that capital injected into R&D doesn't immediately reflect in revenue. Instead, the strongest correlation emerges exactly six months after the initial spend.",
            "Restructure milestone funding. Do not penalize R&D project managers for flat revenue in the immediate quarter following a budget increase."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr class='horizontal-rule'>", unsafe_allow_html=True)

    # ROW 2: Corporate Security & Supply Chain Clusters
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="vertical-rule">', unsafe_allow_html=True)
        render_headline("Silver Lining", "Corporate Security")
        sec_imp = p1['sec_impact']
        
        render_big_number(f"{abs(sec_imp['Tech_Deployments_Coef']):.1f}", "x")
        
        render_story_text(
            f"WAYNE TECH significantly outperforms philanthropy in direct crime reduction. Multivariate regression isolates the exact impact of our interventions. For every additional Tech Deployment, security incidents drop by a factor of {abs(sec_imp['Tech_Deployments_Coef']):.2f}. Community events also help (dropping incidents by {abs(sec_imp['Community_Engagement_Coef']):.2f}), but technological hardware is mathematically superior.",
            "Shift 30% of the philanthropic community budget directly into hardware and software Wayne Tech deployments in high-risk districts like The Narrows."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="col-padding-left">', unsafe_allow_html=True)
        render_headline("Role Reversal", "Supply Chain Efficiency")
        render_chart_subtitle("Quality Score Distribution by Cluster")
        df_sup = p1['df_sup_clustered']
        fig_sup = px.box(df_sup, x='Efficiency_Cluster', y='Quality_Score_Pct', color='Efficiency_Cluster', color_discrete_sequence=MINT_COLORS)
        st.plotly_chart(apply_plotly_theme(fig_sup), use_container_width=True)
        render_story_text(
            "OPERATIONAL DISPARITIES were exposed across facilities using K-Means Clustering. Our machine learning algorithm grouped facilities into distinct efficiency tiers based on lead times and disruption rates. The data overwhelmingly proves that facilities in the top 'Efficiency Cluster' produce significantly higher quality output.",
            "Implement a 'Metropolis Standard' protocol. Mandate underperforming facilities to adopt the logistical routing software used exclusively by top-tier facilities."
        )
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: Predictive Analytics ---
with tab_pred:
    st.markdown('<div class="newspaper-sub-header">PLAIN FACTS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <span class="in-charts-badge">IN CHARTS</span>
        <span class="deep-dive-title">PREDICTIVE DEEP DIVE</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr class='horizontal-rule'>", unsafe_allow_html=True)

    # ROW 3: Threat Forecasting & Innovation Probabilities
    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="vertical-rule">', unsafe_allow_html=True)
        render_headline("Headwinds Ahead?", "Threat Forecasting")
        render_chart_subtitle("Next-Month Security Incident Forecast")
        sec_f = p2['sec_forecast']
        districts = data['security']['District'].unique()
        df_f = pd.DataFrame({'District': districts, 'Forecasted_Incidents': sec_f})
        fig_f = px.bar(df_f, x='District', y='Forecasted_Incidents', color='District', color_discrete_sequence=MINT_COLORS)
        fig_f.update_layout(xaxis=dict(tickangle=-45)) 
        st.plotly_chart(apply_plotly_theme(fig_f), use_container_width=True)
        render_story_text(
            "RANDOM FOREST modeling anticipates an escalation in The Narrows. Feeding historical crime data, spatial geometries, and technological deployment rates into our regressor allows us to forecast next month's incidents. The algorithm flags a persistent, high-volume threat remaining in specific urban districts.",
            "Pre-emptively stage rapid-response teams in the highest forecasted districts before the start of the next calendar month."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="col-padding-left">', unsafe_allow_html=True)
        render_headline("Strategic Focus", "Innovation Probabilities")
        render_chart_subtitle("Probability of Commercialization (%)")
        df_p = p2['project_preds']
        if df_p is not None:
            top_10 = df_p.sort_values('Success_Probability', ascending=False).head(10)
            fig_p = px.bar(top_10, x='Success_Probability', y='Project_Name', orientation='h', color='Success_Probability', color_continuous_scale='Greys')
            fig_p.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(apply_plotly_theme(fig_p), use_container_width=True)
        render_story_text(
            "MACHINE LEARNING successfully isolates top viable R&D projects. Not all R&D is created equal. Using historical completion data, we trained a classification model to output the percentage likelihood of success for currently active projects. The model penalizes bloated budgets and rewards rapid prototyping.",
            "Immediately halt funding for projects with a success probability below 30%. Reallocate capital reserves to the top projects to accelerate time-to-market."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr class='horizontal-rule'>", unsafe_allow_html=True)

    # ROW 4: Human Capital Retention & Supply Chain Risk
    c7, c8 = st.columns(2)
    with c7:
        st.markdown('<div class="vertical-rule">', unsafe_allow_html=True)
        render_headline("Talent Drain", "Human Capital Retention")
        render_chart_subtitle("Turnover Hazard Ratios (< 1.0 Reduces Risk)")
        df_hr_haz = p2['hr_hazard']
        if df_hr_haz is not None:
            df_hr_haz = df_hr_haz.reset_index().rename(columns={'index': 'Feature', 'exp(coef)': 'Hazard_Ratio'})
            name_map = {
                'Benefits_Utilization_Pct': 'Benefits Utilization Rate',
                'Training_Hours_Annual': 'Annual Training Hours',
                'Employee_Satisfaction_Score': 'Employee Satisfaction Score'
            }
            df_hr_haz['Feature'] = df_hr_haz['Feature'].map(name_map).fillna(df_hr_haz['Feature'])
            fig_hr = px.bar(df_hr_haz, x='Hazard_Ratio', y='Feature', orientation='h', color_discrete_sequence=['#be1e2d'])
            fig_hr.add_vline(x=1.0, line_dash="dash", line_color="black")
            st.plotly_chart(apply_plotly_theme(fig_hr), use_container_width=True)
        render_story_text(
            "COX PROPORTIONAL hazards model decodes turnover drivers. Survival analysis isolates how specific employee benefits and training programs affect the risk of resignation. A Hazard Ratio below 1.0 indicates a reduction in attrition risk. The model proves high Employee Satisfaction is the strongest buffer.",
            "Implement targeted benefits awareness campaigns in departments with declining retention rates."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with c8:
        st.markdown('<div class="col-padding-left">', unsafe_allow_html=True)
        render_headline("Hidden Costs", "Supply Chain Shocks")
        render_chart_subtitle("Simulated Distribution of Average Cost Per Unit")
        mc = p2['mc_results']
        fig_mc = px.histogram(mc, x='Avg_Cost', nbins=40, color_discrete_sequence=['#4b5563'])
        fig_mc.add_vline(x=mc['Avg_Cost'].mean(), line_dash="dash", line_color="black")
        fig_mc.add_vline(x=np.percentile(mc['Avg_Cost'], 95), line_dash="solid", line_color="#be1e2d")
        st.plotly_chart(apply_plotly_theme(fig_mc), use_container_width=True)
        render_story_text(
            "MONTE CARLO simulation exposes massive downside cost risks. By running 1,000 randomized 12-month simulations based on our historical disruption variance, we modeled the worst-case scenarios for supply chain costs. The distribution shows a long tail of catastrophic cost spikes if global logistics fail.",
            "Do not plan for the 'Average Cost'. Build cash reserves to withstand the 95th percentile cost curve to ensure uninterrupted operations during global crises."
        )
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: Strategy ---
with tab_strat:
    st.markdown('<div class="newspaper-sub-header">PLAIN FACTS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <span class="in-charts-badge">IN CHARTS</span>
        <span class="deep-dive-title">STRATEGY DEEP DIVE</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr class='horizontal-rule'>", unsafe_allow_html=True)

    # ROW 5: Resource Optimization & Innovation Efficiency
    c9, c10 = st.columns(2)
    with c9:
        st.markdown('<div class="vertical-rule">', unsafe_allow_html=True)
        render_headline("Capital Allocation", "Resource Optimization")
        render_chart_subtitle("Linear Programming Optimization Table")
        ra = p3['resource_allocation']
        st.markdown("""<style>[data-testid="stDataFrame"] {font-family: 'Inter', sans-serif; font-size: 1.0rem;}</style>""", unsafe_allow_html=True)
        st.dataframe(ra.style.format({'Optimal_Multiplier': "{:.2f}", 'Current_Avg_Cost': "${:.2f}M", 'Proposed_Cost': "${:.2f}M"}), use_container_width=True)
        render_story_text(
            "LINEAR PROGRAMMING algorithm dictates optimal capital redistribution. We ran an optimization model to maximize enterprise Net Profit, constrained by maximum operating costs and minimum safety requirements. The model explicitly tells us exactly how much to scale each division.",
            "Execute the 'Optimal Multiplier'. If a division's multiplier is 1.20, increase their operating budget by exactly 20% next quarter."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with c10:
        st.markdown('<div class="col-padding-left">', unsafe_allow_html=True)
        render_headline("Lean Innovators", "Innovation Efficiency")
        render_chart_subtitle("Patents Generated vs. Budget Spent ($M)")
        ino = p3['innovation_data']
        fig_ino = px.scatter(ino, x='Budget_Spent_M', y='Patent_Applications', color='Division', hover_data=['Project_Name', 'Status'], size_max=15, color_discrete_sequence=MINT_COLORS)
        fig_ino.add_shape(type="rect", x0=ino['Budget_Spent_M'].min(), y0=ino['Patent_Applications'].median(), x1=ino['Budget_Spent_M'].median(), y1=ino['Patent_Applications'].max()*1.1, fillcolor="rgba(16, 185, 129, 0.1)", line_width=0)
        fig_ino.update_layout(xaxis_title="Budget Spent ($M)", yaxis_title="Patent Applications")
        st.plotly_chart(apply_plotly_theme(fig_ino), use_container_width=True)
        render_story_text(
            "PLOTTING PATENT applications against Budget Spent reveals highly efficient outliers. The top-left quadrant represents teams generating massive intellectual property while burning minimal cash.",
            "Identify the project managers in the top-left quadrant and promote them to direct underperforming, high-budget projects."
        )
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<hr class='horizontal-rule'>
<div style="text-align: center; font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #666; margin-top: 20px; padding-bottom: 50px;">
    <i>Data points sourced from Wayne Enterprises Global Operations Matrix. Analytics performed by Fox Applied Sciences.</i>
</div>
""", unsafe_allow_html=True)
