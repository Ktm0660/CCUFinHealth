"""Financial health analytics utilities."""
from __future__ import annotations

from typing import List

from .exceptions import AnalysisError
from ..schemas.profile import FinancialHealthReport, FinancialProfile


def calculate_debt_to_income(profile: FinancialProfile) -> float:
    """Return the debt-to-income ratio based on monthly obligations."""

    if profile.monthly_income == 0:
        raise AnalysisError("Monthly income must be greater than zero to compute debt-to-income ratio.")

    total_debt_payments = sum(debt.minimum_payment for debt in profile.debts)
    return total_debt_payments / profile.monthly_income


def calculate_emergency_fund_months(profile: FinancialProfile) -> float:
    """Return the number of months the emergency fund can cover expenses."""

    if profile.monthly_expenses == 0:
        raise AnalysisError("Monthly expenses must be greater than zero to compute emergency fund coverage.")

    return profile.emergency_fund / profile.monthly_expenses


def calculate_savings_goal_progress(profile: FinancialProfile) -> float:
    """Return the average progress across all savings goals."""

    if not profile.savings_goals:
        return 0.0

    total_progress = 0.0
    for goal in profile.savings_goals:
        if goal.target_amount == 0:
            raise AnalysisError(f"Savings goal '{goal.name}' must have a target amount greater than zero.")
        total_progress += min(goal.current_amount / goal.target_amount, 1.0)

    return total_progress / len(profile.savings_goals)


def build_recommendations(report: FinancialHealthReport) -> List[str]:
    """Generate actionable recommendations based on report metrics."""

    recommendations: List[str] = []

    if report.debt_to_income_ratio > 0.35:
        recommendations.append(
            "Consider strategies to lower monthly debt obligations or increase income to improve your debt-to-income ratio."
        )

    if report.emergency_fund_months < 3:
        recommendations.append(
            "Build additional emergency savings to cover at least three months of expenses."
        )

    if report.savings_goal_progress < 0.5:
        recommendations.append(
            "Review savings goals and automate contributions to accelerate progress."
        )

    if report.credit_utilization is not None and report.credit_utilization > 0.3:
        recommendations.append("Aim to keep credit utilization below 30% to maintain strong credit health.")

    if not recommendations:
        recommendations.append("Your financial health indicators look strong. Keep up the good habits!")

    return recommendations


def generate_report(profile: FinancialProfile) -> FinancialHealthReport:
    """Build a full financial health report for the given member profile."""

    debt_to_income = calculate_debt_to_income(profile)
    emergency_fund_months = calculate_emergency_fund_months(profile)
    goal_progress = calculate_savings_goal_progress(profile)

    report = FinancialHealthReport(
        member_id=profile.member_id,
        debt_to_income_ratio=round(debt_to_income, 4),
        emergency_fund_months=round(emergency_fund_months, 2),
        savings_goal_progress=round(goal_progress, 4),
        credit_utilization=profile.credit_utilization,
        recommendations=[],
    )

    report.recommendations = build_recommendations(report)
    return report
