"""API routes for the CCU Financial Health Platform."""
from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, HTTPException, status

from ..schemas.profile import FinancialHealthReport, FinancialProfile
from ..services import analysis
from ..services.exceptions import AnalysisError, handle_analysis_error

router = APIRouter(prefix="/api", tags=["financial-health"])

# In-memory store to support early prototyping
_FAKE_PROFILE_STORE: Dict[str, FinancialProfile] = {}


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Simple heartbeat endpoint."""

    return {"status": "ok"}


@router.post("/profiles", response_model=FinancialProfile, status_code=status.HTTP_201_CREATED)
def upsert_profile(profile: FinancialProfile) -> FinancialProfile:
    """Create or update a member's financial profile."""

    _FAKE_PROFILE_STORE[profile.member_id] = profile
    return profile


@router.get("/profiles/{member_id}", response_model=FinancialProfile)
def get_profile(member_id: str) -> FinancialProfile:
    """Return the stored financial profile for the requested member."""

    try:
        return _FAKE_PROFILE_STORE[member_id]
    except KeyError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found") from exc


@router.post("/reports", response_model=FinancialHealthReport)
def create_report(profile: FinancialProfile) -> FinancialHealthReport:
    """Generate a financial health report from the provided profile payload."""

    try:
        return analysis.generate_report(profile)
    except AnalysisError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=handle_analysis_error(error)) from error
