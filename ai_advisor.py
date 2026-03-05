import streamlit as st
import google.generativeai as genai

def _build_prompt(financial_data: dict) -> str:
    """Build a detailed prompt for personal finance advice suitable for a Hackathon Demo."""
    return f"""
You are a senior AI Financial Advisor. Provide a comprehensive, high-quality financial roadmap based on:
- Monthly Income: ₹{financial_data.get('monthly_income', 0):,.2f}
- Monthly Expenses: ₹{financial_data.get('monthly_expenses', 0):,.2f} (Ratio: {(financial_data.get('monthly_expenses', 0)/financial_data.get('monthly_income', 1))*100:.1f}%)
- Monthly Savings: ₹{financial_data.get('monthly_savings', 0):,.2f} (Rate: {financial_data.get('savings_rate', 0):.1f}%)
- Current Total Savings: ₹{financial_data.get('current_savings', 0):,.2f}
- Existing Debt: ₹{financial_data.get('total_debt', 0):,.2f}
- Financial Goal: {financial_data.get('goal', 'N/A')}
- Goal Target: ₹{financial_data.get('goal_amount', 0):,.2f}
- Monthly Savings Target for Goal: ₹{financial_data.get('required_monthly_savings', 0):,.2f}

Structure your response into the following sections using bullet points:
1. **Budget Improvement Suggestions**: Identify areas for optimization.
2. **Investment Recommendations**: List 3-4 suitable investment paths based on their profile.
3. **Debt Reduction Strategy**: Provide a clear plan to handle existing debt.
4. **Goal Achievement Plan**: A step-by-step roadmap to hit their ₹{financial_data.get('goal_amount', 0):,.2f} target.

Make the advice data-driven, professional, and encouraging.
"""

def get_financial_advice(financial_data: dict) -> str:
    """Generate advice using Gemini with Streamlit Secrets and quota error handling."""
    
    # Secure API Key loading from Streamlit Secrets
    if "GEMINI_API_KEY" not in st.secrets:
        return (
            "⚠️ **API Key Not Configured**\n\n"
            "Please add `GEMINI_API_KEY` in Streamlit Secrets (Cloud) or `.streamlit/secrets.toml` (Local)."
        )

    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    # Initialize the supported Gemini 2.0 Flash model
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = _build_prompt(financial_data)

    try:
        response = model.generate_content(prompt)
        advice = response.text
    except Exception as e:
        # Proper error handling for quota or API service issues
        advice = f"AI service temporarily unavailable: {e}"
    
    return advice
