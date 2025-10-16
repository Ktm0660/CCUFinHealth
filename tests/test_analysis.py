"""Unit tests for financial analysis utilities."""
from app.schemas.profile import Debt, FinancialProfile, SavingsGoal
from app.services import analysis
from app.services.exceptions import AnalysisError


def sample_profile() -> FinancialProfile:
    return FinancialProfile(
        member_id="123",
        monthly_income=6000,
        monthly_expenses=3500,
        emergency_fund=7000,
        debts=[
            Debt(name="Auto Loan", balance=12000, interest_rate=3.5, minimum_payment=300),
            Debt(name="Credit Card", balance=4500, interest_rate=18.9, minimum_payment=150),
        ],
        savings_goals=[
            SavingsGoal(name="Vacation", target_amount=2000, current_amount=500),
            SavingsGoal(name="Home Down Payment", target_amount=30000, current_amount=6000),
        ],
        credit_utilization=0.4,
    )


def test_generate_report_success():
    profile = sample_profile()

    report = analysis.generate_report(profile)

    assert report.member_id == profile.member_id
    assert report.debt_to_income_ratio == round((300 + 150) / 6000, 4)
    assert report.emergency_fund_months == round(7000 / 3500, 2)
    assert report.savings_goal_progress == round(((0.25 + 0.2) / 2), 4)
    assert "debt" in " ".join(report.recommendations).lower()


def test_generate_report_handles_zero_income():
    profile = sample_profile()
    profile.monthly_income = 0

    try:
        analysis.generate_report(profile)
    except AnalysisError as error:
        assert "income" in str(error).lower()
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected AnalysisError for zero income")


def test_generate_report_handles_zero_expenses():
    profile = sample_profile()
    profile.monthly_expenses = 0

    try:
        analysis.generate_report(profile)
    except AnalysisError as error:
        assert "expenses" in str(error).lower()
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected AnalysisError for zero expenses")
