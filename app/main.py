"""Application entrypoint for the CCU Financial Health Platform."""
from __future__ import annotations

from fastapi import FastAPI

from .api.routes import router as api_router

app = FastAPI(title="CCU Financial Health Platform", version="0.1.0")
app.include_router(api_router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    """Provide a simple welcome message for quick smoke testing."""

    return {"message": "Welcome to the CCU Financial Health Platform API"}
