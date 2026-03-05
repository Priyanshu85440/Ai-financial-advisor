"""
Goal-Based Planning Module
===========================
Helps users plan toward specific financial goals by calculating required
monthly savings and assessing whether the goal is feasible given current
cash flow.
"""


def calculate_monthly_goal_savings(goal_amount: float, years: float) -> float:
    """
    Calculate the monthly savings required to reach a financial goal.

    Formula: goal_amount / (years × 12)
    Returns 0.0 if years is zero or negative.
    """
    if years <= 0:
        return 0.0
    total_months = years * 12
    return round(goal_amount / total_months, 2)


def assess_goal_feasibility(
    monthly_savings: float, required_monthly: float
) -> dict:
    """
    Assess whether the user can achieve their goal with current savings rate.

    Returns a dict with:
        - is_feasible (bool): True if monthly_savings >= required_monthly
        - surplus_or_deficit (float): positive = surplus, negative = deficit
        - message (str): human-readable feasibility statement
    """
    difference = monthly_savings - required_monthly

    if difference >= 0:
        return {
            "is_feasible": True,
            "surplus_or_deficit": round(difference, 2),
            "message": (
                f"✅ You are on track! You have a surplus of ₹{difference:,.2f} "
                f"per month beyond what is needed."
            ),
        }
    else:
        return {
            "is_feasible": False,
            "surplus_or_deficit": round(difference, 2),
            "message": (
                f"⚠️ You need to save an additional ₹{abs(difference):,.2f} "
                f"per month to reach your goal on time."
            ),
        }


def get_goal_plan(
    goal: str, goal_amount: float, years: float, monthly_savings: float
) -> dict:
    """
    Build a complete goal plan summary.

    Parameters
    ----------
    goal            : Description of the financial goal
    goal_amount     : Target amount in ₹
    years           : Time horizon in years
    monthly_savings : User's current monthly savings (income − expenses)

    Returns
    -------
    dict with goal details, required savings, and feasibility assessment.
    """
    required_monthly = calculate_monthly_goal_savings(goal_amount, years)
    feasibility = assess_goal_feasibility(monthly_savings, required_monthly)

    return {
        "goal": goal,
        "goal_amount": goal_amount,
        "time_horizon_years": years,
        "total_months": int(years * 12),
        "required_monthly_savings": required_monthly,
        "current_monthly_savings": monthly_savings,
        **feasibility,
    }
