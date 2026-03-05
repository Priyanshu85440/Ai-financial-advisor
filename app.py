import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from financial_analysis import get_financial_summary
from goal_planner import get_goal_plan
from ai_advisor import get_financial_advice

# ---------------------------------------------------------------------------
# Page configuration - No Sidebar by default
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="stApp"] { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    .main-header { text-align: center; padding: 1rem; color: #7dd3fc; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); 
        border-radius: 12px; 
        padding: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .section-title { color: #a78bfa; font-weight: 800; font-size: 1.5rem; margin-top: 1rem; margin-bottom: 1rem; }
    /* Hide Sidebar completely */
    [data-testid="stSidebar"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="main-header"><h1>🚀 AI Financial Advisor</h1><p style="color: #94a3b8; font-size: 1.2rem;">Smart insights powered by Google Gemini</p></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Landing Page Welcome & Initial Button
# ---------------------------------------------------------------------------
if not st.session_state.show_form:
    st.info("👋 Welcome! Let's get started on your personalized financial roadmap.")
    
    welcome_col1, welcome_col2 = st.columns(2)
    with welcome_col1:
        st.markdown("""
        ### Why use AI Financial Advisor?
        - **Precision**: Deep math for your health scores.
        - **Visuals**: Plotly-powered interactive charts.
        - **AI Intelligence**: Powered by Gemini 2.0 Flash for bespoke advice.
        """)
    with welcome_col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=200)

    st.markdown("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🔍 Check Financial Status", use_container_width=True, type="primary"):
            st.session_state.show_form = True
            st.rerun()

# ---------------------------------------------------------------------------
# Financial Input Form (Shown after clicking the first button)
# ---------------------------------------------------------------------------
if st.session_state.show_form and not st.session_state.show_results:
    st.markdown('<div class="section-title">📝 Financial Profile Details</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            income = st.number_input("Monthly Income (₹)", min_value=0.0, value=75000.0, step=1000.0)
            expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=35000.0, step=1000.0)
            savings = st.number_input("Current Savings (₹)", min_value=0.0, value=250000.0, step=5000.0)
        
        with col_f2:
            debt = st.number_input("Existing Debt (₹)", min_value=0.0, value=50000.0, step=1000.0)
            goal_text = st.text_input("Goal Name", value="Dream Home Downpayment")
            goal_amt = st.number_input("Goal Target (₹)", min_value=0.0, value=1500000.0, step=50000.0)
            years = st.slider("Time Horizon (Years)", 1, 30, 5)
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns([1, 2, 1])
    with bc2:
        if st.button("🚀 Analyze My Finances", use_container_width=True, type="primary"):
            st.session_state.show_results = True
            # We need to store these inputs in session state to persist them for analysis
            st.session_state.income = income
            st.session_state.expenses = expenses
            st.session_state.savings = savings
            st.session_state.debt = debt
            st.session_state.goal_text = goal_text
            st.session_state.goal_amt = goal_amt
            st.session_state.years = years
            st.rerun()

# ---------------------------------------------------------------------------
# Results Section (Shown after clicking Analyze)
# ---------------------------------------------------------------------------
if st.session_state.show_results:
    # Retrieve inputs from session state
    income = st.session_state.income
    expenses = st.session_state.expenses
    savings = st.session_state.savings
    debt = st.session_state.debt
    goal_text = st.session_state.goal_text
    goal_amt = st.session_state.goal_amt
    years = st.session_state.years

    # Calculations
    summary = get_financial_summary(income, expenses, savings, debt)
    plan = get_goal_plan(goal_text, goal_amt, years, summary["monthly_savings"], current_savings=savings)
    
    # 1. Financial Health Score & Top Metrics
    st.markdown('<div class="section-title">✨ Financial Health Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    score = summary["health_score"]
    color = "normal" if score > 80 else ("off" if score > 50 else "inverse")
    
    with col1:
        st.metric("Health Score", f"{score}/100", delta=f"{score-50}% vs Avg", delta_color=color)
    with col2:
        st.metric("Savings Rate", f"{summary['savings_rate']}%", delta="High" if summary['savings_rate'] > 20 else "Low")
    with col3:
        st.metric("Debt-to-Income", f"{summary['debt_to_income']}%", delta="Risky" if summary['debt_to_income'] > 40 else "Safe", delta_color="inverse")
    with col4:
        st.metric("Monthly Surplus", f"₹{summary['monthly_savings']:,.0f}")

    # 2. Progress Bars
    st.markdown("---")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("💡 Savings Capability")
        st.write(f"You save **{summary['savings_rate']}%** of your monthly income.")
        st.progress(min(summary['savings_rate']/100, 1.0))
        if summary['savings_rate'] >= 20:
            st.success("Great job! You are exceeding the 20% savings rule.")
        else:
            st.warning("Try to cut expenses to hit at least a 20% savings rate.")

    with res_col2:
        st.subheader(f"🎯 Goal: {goal_text}")
        st.write(f"You have achieved **{plan['goal_progress']}%** of your ₹{goal_amt:,.0f} target.")
        st.progress(plan['goal_progress']/100)
        st.info(plan["message"])

    # 3. Visualizations
    st.markdown('<div class="section-title">📈 Visual Analytics</div>', unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Expenses', 'Savings', 'Debt'],
            values=[expenses, max(summary['monthly_savings'], 0), debt],
            hole=.4,
            marker_colors=['#f87171', '#34d399', '#fbbf24']
        )])
        fig_pie.update_layout(title_text="Portfolio Distribution", template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with chart_col2:
        categories = ['Income', 'Expenses', 'Savings']
        values = [income, expenses, summary['monthly_savings']]
        fig_bar = go.Figure([go.Bar(x=categories, y=values, marker_color=['#7dd3fc', '#f472b6', '#34d399'])])
        fig_bar.update_layout(title_text="Monthly Cashflow", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

    # 4. AI Advice
    st.markdown('<div class="section-title">🤖 AI Financial Insights</div>', unsafe_allow_html=True)
    ai_data = {**summary, **plan}
    with st.spinner("Consulting with Gemini AI..."):
        advice = get_financial_advice(ai_data)
        st.markdown(f'<div class="glass-card">{advice}</div>', unsafe_allow_html=True)

    # Reset Button to redo inputs
    if st.button("🔄 Restart Analysis", use_container_width=True):
        st.session_state.show_form = False
        st.session_state.show_results = False
        st.rerun()
