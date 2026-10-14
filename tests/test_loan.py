from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_loan_approved():
    response = client.post("/api/v1/loans/apply", json={
        "full_name": "Prince Anand",
        "monthly_income": 60000.0,
        "credit_score": 780,
        "employment_type": "SALARIED"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "APPROVED"
    assert data["approved_amount"] == 600000.0

def test_loan_rejected_low_credit_score():
    response = client.post("/api/v1/loans/apply", json={
        "full_name": "Ankit Singh",
        "monthly_income": 80000.0,
        "credit_score": 600,
        "employment_type": "SALARIED"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "REJECTED"
    assert "below minimum risk cut-off" in data["rejection_reason"]