"""Pydantic schemas for user financial data."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class Debt(BaseModel):
    """Represents a single debt account."""

    name: str = Field(..., description="Name of the debt account")
    balance: float = Field(..., ge=0, description="Current outstanding balance")
    interest_rate: float = Field(..., ge=0, description="Annual interest rate as a percentage")
    minimum_payment: float = Field(..., ge=0, description="Required minimum monthly payment")


class SavingsGoal(BaseModel):
    """Represents a savings goal with target and progress."""

    name: str
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(0, ge=0)
    target_date: Optional[date] = None


class FinancialProfile(BaseModel):
    """Aggregated view of a member's financial position."""

    member_id: str
    monthly_income: float = Field(..., ge=0)
    monthly_expenses: float = Field(..., ge=0)
    emergency_fund: float = Field(..., ge=0)
    debts: List[Debt] = Field(default_factory=list)
    savings_goals: List[SavingsGoal] = Field(default_factory=list)
    credit_utilization: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Credit utilization ratio (0 to 1)",
    )


class FinancialHealthReport(BaseModel):
    """Summary of key financial health indicators."""

    member_id: str
    debt_to_income_ratio: float
    emergency_fund_months: float
    savings_goal_progress: float
    credit_utilization: Optional[float]
    recommendations: List[str]
