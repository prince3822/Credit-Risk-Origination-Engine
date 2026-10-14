import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

def generate_reference_id():
    return f"APP-{datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(String, unique=True, index=True, default=generate_reference_id)
    applicant_name = Column(String, nullable=False)
    monthly_income = Column(Float, nullable=False)
    credit_score = Column(Integer, nullable=False)
    employment_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    approved_limit = Column(Float, default=0.0)
    rejection_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)