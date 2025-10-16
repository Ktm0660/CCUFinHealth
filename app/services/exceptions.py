"""Custom exceptions for analysis services."""


class AnalysisError(ValueError):
    """Raised when the provided financial data is insufficient for analysis."""


def handle_analysis_error(error: AnalysisError) -> dict[str, str]:
    """Standardize error responses for the API layer."""

    return {"detail": str(error)}
