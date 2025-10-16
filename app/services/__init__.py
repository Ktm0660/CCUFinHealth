"""Service layer exports."""

from .analysis import (
    build_recommendations,
    calculate_debt_to_income,
    calculate_emergency_fund_months,
    calculate_savings_goal_progress,
    generate_report,
)
from .exceptions import AnalysisError

__all__ = [
    "AnalysisError",
    "build_recommendations",
    "calculate_debt_to_income",
    "calculate_emergency_fund_months",
    "calculate_savings_goal_progress",
    "generate_report",
]
