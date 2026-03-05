"""
AI Financial Advisor — Streamlit Dashboard
============================================
Main entry-point that ties together the financial analysis module,
goal planner, AI advisor (Gemini 2.0 Flash), and interactive Plotly charts
into a polished, premium-looking dashboard.

Run with:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go

from financial_analysis import get_financial_summary
from goal_planner import get_goal_plan
from ai_advisor import get_financial_advice

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — premium dark-gradient theme with glassmorphism cards
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="stApp"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161637 0%, #1e1e4a 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #a78bfa;
    }

    /* ---------- Header ---------- */
    .main-header {
        text-align: center;
        padding: 2rem 1rem 1rem;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #7dd3fc, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 1.1rem;
    }

    /* ---------- Glass card ---------- */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.6rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(12px);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(167, 139, 250, 0.15);
    }

    /* ---------- Metric cards ---------- */
    .metric-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .metric-card {
        flex: 1;
        min-width: 200px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-card .label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card .value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #e2e8f0;
    }
    .metric-card .value.positive { color: #34d399; }
    .metric-card .value.negative { color: #f87171; }
    .metric-card .value.warning  { color: #fbbf24; }

    /* ---------- Section title ---------- */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #c4b5fd;
        margin: 1.8rem 0 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ---------- Feasibility ---------- */
    .feasibility-box {
        padding: 1rem 1.4rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
    }
    .feasibility-ok  { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
    .feasibility-bad { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }

    /* ---------- AI advice ---------- */
    .ai-advice {
        background: rgba(167,139,250,0.06);
        border: 1px solid rgba(167,139,250,0.15);
        border-radius: 16px;
        padding: 1.6rem;
        color: #e2e8f0;
        line-height: 1.7;
    }
    .ai-advice h1, .ai-advice h2, .ai-advice h3 {
        color: #c4b5fd;
    }

    /* ---------- Hide Streamlit branding ---------- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>💹 AI Financial Advisor</h1>
        <p>Smart insights powered by Google Gemini · Plan · Save · Grow</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar — Input Form
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📋 Your Financial Profile")

    st.markdown("#### 💵 Income & Expenses")
    monthly_income = st.number_input(
        "Monthly Income (₹)", min_value=0.0, value=50000.0, step=1000.0,
        format="%.2f", key="income"
    )
    monthly_expenses = st.number_input(
        "Monthly Expenses (₹)", min_value=0.0, value=30000.0, step=1000.0,
        format="%.2f", key="expenses"
    )

    st.markdown("#### 🏦 Savings & Debt")
    current_savings = st.number_input(
        "Current Savings (₹)", min_value=0.0, value=100000.0, step=5000.0,
        format="%.2f", key="savings"
    )
    existing_debt = st.number_input(
        "Existing Debt (₹)", min_value=0.0, value=0.0, step=5000.0,
        format="%.2f", key="debt"
    )

    st.markdown("#### 🎯 Financial Goal")
    financial_goal = st.text_input(
        "Describe your goal", value="Buy a house", key="goal"
    )
    goal_amount = st.number_input(
        "Goal Amount (₹)", min_value=0.0, value=500000.0, step=10000.0,
        format="%.2f", key="goal_amount"
    )
    time_horizon = st.number_input(
        "Time Horizon (years)", min_value=0.5, value=3.0, step=0.5,
        format="%.1f", key="horizon"
    )

    st.markdown("---")
    analyze_btn = st.button("🚀  Analyze My Finances", use_container_width=True)

# ---------------------------------------------------------------------------
# Main area — results (shown only after user clicks Analyze)
# ---------------------------------------------------------------------------
if analyze_btn:
    # ---- Financial analysis -------------------------------------------------
    summary = get_financial_summary(
        monthly_income, monthly_expenses, current_savings, existing_debt
    )

    # ---- Goal planning ------------------------------------------------------
    plan = get_goal_plan(
        financial_goal, goal_amount, time_horizon, summary["monthly_savings"]
    )

    # ---- Display metric cards -----------------------------------------------
    st.markdown('<div class="section-title">📊 Financial Health Snapshot</div>', unsafe_allow_html=True)

    savings_class = "positive" if summary["monthly_savings"] >= 0 else "negative"
    rate_class = "positive" if summary["savings_rate"] >= 20 else ("warning" if summary["savings_rate"] >= 10 else "negative")
    dti_class = "positive" if summary["debt_to_income"] <= 30 else ("warning" if summary["debt_to_income"] <= 50 else "negative")

    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="label">Monthly Savings</div>
                <div class="value {savings_class}">₹{summary['monthly_savings']:,.2f}</div>
            </div>
            <div class="metric-card">
                <div class="label">Savings Rate</div>
                <div class="value {rate_class}">{summary['savings_rate']:.1f}%</div>
            </div>
            <div class="metric-card">
                <div class="label">Debt-to-Income</div>
                <div class="value {dti_class}">{summary['debt_to_income']:.1f}%</div>
            </div>
            <div class="metric-card">
                <div class="label">Current Savings</div>
                <div class="value">₹{summary['current_savings']:,.2f}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Goal Plan ----------------------------------------------------------
    st.markdown('<div class="section-title">🎯 Goal Plan</div>', unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="metric-card" style="background:transparent;border:none;">
                    <div class="label">Required Monthly Savings</div>
                    <div class="value" style="color:#7dd3fc;">₹{plan['required_monthly_savings']:,.2f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_g2:
        feas_class = "feasibility-ok" if plan["is_feasible"] else "feasibility-bad"
        st.markdown(
            f'<div class="feasibility-box {feas_class}">{plan["message"]}</div>',
            unsafe_allow_html=True,
        )

    # ---- Charts (Plotly) ----------------------------------------------------
    st.markdown('<div class="section-title">📈 Visual Insights</div>', unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)

    # -- Pie chart: Expenses vs Savings distribution --------------------------
    with col_c1:
        pie_labels = ["Expenses", "Savings"]
        pie_values = [
            monthly_expenses,
            max(summary["monthly_savings"], 0),
        ]
        pie_colors = ["#f87171", "#34d399"]

        fig_pie = go.Figure(
            go.Pie(
                labels=pie_labels,
                values=pie_values,
                hole=0.55,
                marker=dict(colors=pie_colors, line=dict(color="#1a1a3e", width=2)),
                textinfo="label+percent",
                textfont=dict(size=13, color="#e2e8f0"),
                hoverinfo="label+value+percent",
            )
        )
        fig_pie.update_layout(
            title=dict(text="Expenses vs Savings", font=dict(color="#c4b5fd", size=16)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#94a3b8")),
            margin=dict(t=50, b=20, l=20, r=20),
            height=370,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # -- Bar chart: Financial health overview ---------------------------------
    with col_c2:
        bar_categories = ["Income", "Expenses", "Savings", "Debt"]
        bar_values = [
            monthly_income,
            monthly_expenses,
            summary["monthly_savings"],
            existing_debt,
        ]
        bar_colors = ["#7dd3fc", "#f87171", "#34d399", "#fbbf24"]

        fig_bar = go.Figure(
            go.Bar(
                x=bar_categories,
                y=bar_values,
                marker=dict(
                    color=bar_colors,
                    line=dict(width=0),
                    cornerradius=6,
                ),
                text=[f"₹{v:,.0f}" for v in bar_values],
                textposition="outside",
                textfont=dict(color="#e2e8f0", size=12),
            )
        )
        fig_bar.update_layout(
            title=dict(text="Financial Health Overview", font=dict(color="#c4b5fd", size=16)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickfont=dict(color="#94a3b8"), showgrid=False),
            yaxis=dict(tickfont=dict(color="#94a3b8"), showgrid=True,
                       gridcolor="rgba(255,255,255,0.05)"),
            margin=dict(t=50, b=20, l=20, r=20),
            height=370,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ---- AI Advice ----------------------------------------------------------
    st.markdown('<div class="section-title">🤖 AI-Powered Financial Advice</div>', unsafe_allow_html=True)

    # Merge summary + plan into one dict for the AI prompt
    ai_data = {**summary, **plan}

    with st.spinner("✨ Generating personalized advice with Gemini 2.0 Flash …"):
        advice = get_financial_advice(ai_data)

    st.markdown(f'<div class="ai-advice">{advice}</div>', unsafe_allow_html=True)

else:
    # --- Welcome state -------------------------------------------------------
    st.markdown(
        """
        <div class="glass-card" style="text-align:center; margin-top:3rem;">
            <p style="font-size:3rem; margin:0;">💰</p>
            <h3 style="color:#c4b5fd; margin:0.5rem 0;">Welcome to AI Financial Advisor</h3>
            <p style="color:#94a3b8;">
                Fill in your financial details in the sidebar and click
                <strong style="color:#a78bfa;">Analyze My Finances</strong> to get
                personalized insights, charts, and AI-powered advice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
