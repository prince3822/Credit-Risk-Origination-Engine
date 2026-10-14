from typing import Tuple, Optional
from app.schemas import EmploymentType

def evaluate_risk_policy(income: float, score: int, emp_type: EmploymentType) -> Tuple[str, float, Optional[str]]:
    # Minimum income check based on employment category
    min_income = 25000.0 if emp_type == EmploymentType.SALARIED else 40000.0

    # Rule 1: Credit score cutoff
    if score < 650:
        return "REJECTED", 0.0, "Credit score falls below minimum risk cut-off (650)."

    # Rule 2: Minimum income cutoff
    if income < min_income:
        return "REJECTED", 0.0, f"Income below threshold ({min_income}) for {emp_type.value} category."

    # Rule 3: Approved limit multiplier
    multiplier = 10 if score >= 750 else 6
    approved_limit = income * multiplier
    return "APPROVED", approved_limit, None