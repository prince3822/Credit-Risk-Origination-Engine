from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class EmploymentType(str, Enum):
    SALARIED = "SALARIED"
    SELF_EMPLOYED = "SELF_EMPLOYED"

class LoanApplyRequest(BaseModel):
    applicant_name: str = Field(..., min_length=2, example="Prince Kumar")
    monthly_income: float = Field(..., gt=0, example=65000.0)
    credit_score: int = Field(..., ge=300, le=900, example=780)
    employment_type: EmploymentType = Field(..., example=EmploymentType.SALARIED)

class LoanDecisionResponse(BaseModel):
    id: int
    reference_id: str
    applicant_name: str
    status: str
    approved_limit: float
    rejection_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True