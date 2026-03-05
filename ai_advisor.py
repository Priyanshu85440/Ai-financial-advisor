import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI using the key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def _build_prompt(financial_data: dict) -> str:
    """Build a personalized financial advice prompt."""
    return f"""
Analyze the following financial profile and provide expert advice:
- Monthly Income: ₹{financial_data.get('monthly_income', 0):,.2f}
- Monthly Expenses: ₹{financial_data.get('monthly_expenses', 0):,.2f}
- Monthly Savings: ₹{financial_data.get('monthly_savings', 0):,.2f}
- Current Savings: ₹{financial_data.get('current_savings', 0):,.2f}
- Existing Debt: ₹{financial_data.get('total_debt', 0):,.2f}
- Financial Goal: {financial_data.get('goal', 'Not specified')} (₹{financial_data.get('goal_amount', 0):,.2f})

Please provide:
1. **Budgeting Advice**: How to manage spending.
2. **Savings Suggestions**: Ways to increase monthly savings.
3. **Investment Recommendations**: Where to put money for growth.
4. **Debt Reduction Strategy**: Best way to pay off existing debt.

Keep the advice practical and motivating.
"""

def get_financial_advice(financial_data: dict) -> str:
    """Generate advice using Gemini with quota error handling."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Gemini API Key Missing. Please add your `GEMINI_API_KEY` to the `.env` file."

    # Use the supported Gemini 2.0 Flash model
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = _build_prompt(financial_data)

    try:
        response = model.generate_content(prompt)
        advice = response.text
    except Exception as e:
        # Proper error handling for quota or API service issues
        advice = f"AI service temporarily unavailable: {e}"
    
    return advice
