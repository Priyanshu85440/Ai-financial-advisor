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


def calculate_goal_progress(current_savings: float, goal_amount: float) -> float:
    """Calculate percentage progress toward the goal amount."""
    if goal_amount <= 0:
        return 0.0
    progress = (current_savings / goal_amount) * 100
    return min(round(progress, 2), 100.0)

def get_goal_plan(
    goal: str, goal_amount: float, years: float, monthly_savings: float, current_savings: float = 0.0
) -> dict:
    """
    Build a complete goal plan summary.
    """
    # Defensive type conversion
    g_amt = float(goal_amount)
    y = float(years)
    m_sav = float(monthly_savings)
    c_sav = float(current_savings)

    required_monthly = calculate_monthly_goal_savings(g_amt, y)
    feasibility = assess_goal_feasibility(m_sav, required_monthly)
    progress = calculate_goal_progress(c_sav, g_amt)

    return {
        "goal": str(goal),
        "goal_amount": g_amt,
        "time_horizon_years": y,
        "total_months": int(y * 12),
        "required_monthly_savings": required_monthly,
        "current_monthly_savings": m_sav,
        "goal_progress": progress,
        **feasibility,
    }
