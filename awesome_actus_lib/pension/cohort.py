from dataclasses import dataclass
from datetime import date
from typing import Literal, Optional

CohortStatus = Literal["active", "retired"]


@dataclass
class Cohort:
    cohort_id: str
    birth_year: int
    headcount: int
    gross_salary: float
    accrued_savings: float
    status: CohortStatus = "active"
    annual_pension: Optional[float] = None

    def current_age(self, as_of: date) -> int:
        return as_of.year - self.birth_year
