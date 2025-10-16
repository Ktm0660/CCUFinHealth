"""Integration tests for FastAPI routes."""
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.profile import Debt, FinancialProfile, SavingsGoal

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_profile_lifecycle():
    profile = FinancialProfile(
        member_id="abc",
        monthly_income=5000,
        monthly_expenses=3200,
        emergency_fund=8000,
        debts=[Debt(name="Car", balance=10000, interest_rate=4.1, minimum_payment=250)],
        savings_goals=[SavingsGoal(name="Emergency", target_amount=12000, current_amount=8000)],
        credit_utilization=0.25,
    )

    create_response = client.post("/api/profiles", json=profile.model_dump(mode="json"))
    assert create_response.status_code == 201
    assert create_response.json()["member_id"] == profile.member_id

    fetch_response = client.get(f"/api/profiles/{profile.member_id}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["member_id"] == profile.member_id


def test_report_generation_endpoint():
    profile_payload = {
        "member_id": "member-1",
        "monthly_income": 4000,
        "monthly_expenses": 2500,
        "emergency_fund": 3000,
        "debts": [
            {
                "name": "Loan",
                "balance": 8000,
                "interest_rate": 5.0,
                "minimum_payment": 200,
            }
        ],
        "savings_goals": [
            {
                "name": "Vacation",
                "target_amount": 1500,
                "current_amount": 600,
            }
        ],
        "credit_utilization": 0.5,
    }

    response = client.post("/api/reports", json=profile_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["member_id"] == profile_payload["member_id"]
    assert body["recommendations"]


def test_report_generation_handles_validation_error():
    profile_payload = {
        "member_id": "member-2",
        "monthly_income": 0,
        "monthly_expenses": 1500,
        "emergency_fund": 2000,
        "debts": [],
        "savings_goals": [],
    }

    response = client.post("/api/reports", json=profile_payload)
    assert response.status_code == 422
    assert "income" in str(response.json()).lower()
