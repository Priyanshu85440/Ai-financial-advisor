"""
Financial Analysis Module
=========================
Provides core financial calculation functions including monthly savings,
savings rate, and debt-to-income ratio. All functions are pure and stateless,
making them easy to test and extend.
"""


def calculate_monthly_savings(income: float, expenses: float) -> float:
    """Calculate the amount saved each month (income minus expenses)."""
    return income - expenses


def calculate_savings_rate(income: float, expenses: float) -> float:
    """
    Calculate savings rate as a percentage of income.
    Returns 0.0 if income is zero to avoid division errors.
    """
    if income <= 0:
        return 0.0
    savings = income - expenses
    return round((savings / income) * 100, 2)


def calculate_debt_to_income(debt: float, income: float) -> float:
    """
    Calculate the debt-to-income ratio as a percentage.
    A lower ratio indicates better financial health.
    Returns 0.0 if income is zero.
    """
    if income <= 0:
        return 0.0
    return round((debt / income) * 100, 2)


def calculate_health_score(income: float, expenses: float, debt: float, savings_rate: float) -> int:
    """
    Calculate a financial health score out of 100.
    - Savings Rate (40%): >20% is ideal
    - Debt-to-Income (30%): <30% is ideal
    - Emergency Fund Base (30%): (Simulated here by savings/expenses ratio)
    """
    score = 0
    
    # Savings Rate component (Max 40)
    score += min(max(savings_rate * 2, 0), 40)
    
    # Debt-to-Income component (Max 30)
    dti = calculate_debt_to_income(debt, income)
    score += max(30 - (dti / 2), 0)
    
    # Expense component (Max 30)
    if income > 0:
        expense_ratio = (expenses / income) * 100
        score += max(30 - (expense_ratio / 3), 0)
    
    return int(min(max(score, 0), 100))

def get_financial_summary(
    income: float, expenses: float, savings: float, debt: float
) -> dict:
    """
    Generate a comprehensive financial summary dictionary.
    """
    monthly_savings = calculate_monthly_savings(income, expenses)
    savings_rate = calculate_savings_rate(income, expenses)
    debt_to_income = calculate_debt_to_income(debt, income)
    health_score = calculate_health_score(income, expenses, debt, savings_rate)

    return {
        "monthly_income": income,
        "monthly_expenses": expenses,
        "monthly_savings": monthly_savings,
        "savings_rate": savings_rate,
        "debt_to_income": debt_to_income,
        "current_savings": savings,
        "total_debt": debt,
        "health_score": health_score
    }
