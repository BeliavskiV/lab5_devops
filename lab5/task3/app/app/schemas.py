from pydantic import BaseModel
from typing import Dict, List

class StudentBase(BaseModel):
    full_name: str
    specialty: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    status: str

    class Config:
        from_attributes = True

class StudentTransfer(BaseModel):
    new_specialty: str

class ReportSummary(BaseModel):
    active_students_by_specialty: Dict[str, int]
    total_active_students: int
    total_expelled_students: int