from fastapi import FastAPI, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import engine, Base, get_db
from app.models import LoanApplication
from app.schemas import LoanApplyRequest, LoanDecisionResponse
from app.service import evaluate_risk_policy

# Creates fresh tables with all columns
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loan Origination & Risk Engine",
    description="Automated Underwriting API for instant loan eligibility checks",
    version="1.0.0"
)

@app.post("/api/v1/loans/apply", response_model=LoanDecisionResponse, status_code=status.HTTP_201_CREATED)
def submit_loan_application(payload: LoanApplyRequest, db: Session = Depends(get_db)):
    status_dec, limit, reason = evaluate_risk_policy(
        income=payload.monthly_income,
        score=payload.credit_score,
        emp_type=payload.employment_type
    )

    record = LoanApplication(
        applicant_name=payload.applicant_name,
        monthly_income=payload.monthly_income,
        credit_score=payload.credit_score,
        employment_type=payload.employment_type.value,
        status=status_dec,
        approved_limit=limit,
        rejection_reason=reason
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record

@app.get("/api/v1/loans/applications", response_model=List[LoanDecisionResponse])
def fetch_applications(status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(LoanApplication)
    if status:
        query = query.filter(LoanApplication.status == status.upper())
    return query.all()