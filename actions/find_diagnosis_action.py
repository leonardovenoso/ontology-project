from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis
from models.staff import Staff
from models.diagnosis import Diagnosis
from queries.find_diagnosis_by_patient_mrn import find_diagnosis_by_patient_mrn

def find_diagnosis(mrn: str, staff: Staff, db_session: Session) -> list[Diagnosis]:
  if staff.role != "doctor":
    raise PermissionError("Invalid role")

  return find_diagnosis_by_patient_mrn(mrn, db_session)