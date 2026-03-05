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


def get_financial_summary(
    income: float, expenses: float, savings: float, debt: float
) -> dict:
    """
    Generate a comprehensive financial summary dictionary.

    Parameters
    ----------
    income   : Monthly income
    expenses : Monthly expenses
    savings  : Current total savings
    debt     : Existing total debt

    Returns
    -------
    dict with keys:
        monthly_savings, savings_rate, debt_to_income,
        current_savings, total_debt, monthly_income, monthly_expenses
    """
    monthly_savings = calculate_monthly_savings(income, expenses)
    savings_rate = calculate_savings_rate(income, expenses)
    debt_to_income = calculate_debt_to_income(debt, income)

    return {
        "monthly_income": income,
        "monthly_expenses": expenses,
        "monthly_savings": monthly_savings,
        "savings_rate": savings_rate,
        "debt_to_income": debt_to_income,
        "current_savings": savings,
        "total_debt": debt,
    }
