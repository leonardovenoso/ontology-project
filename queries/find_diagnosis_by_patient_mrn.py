from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis
from models.patient import Patient
from queries.find_patient_by_mrn import find_patient_by_mrn

def find_diagnosis_by_patient_mrn(mrn: str, db_session: Session) -> list[Diagnosis]:
  patient = find_patient_by_mrn(mrn, db_session)
  
  if patient is None:
    return []

  diagnosis: list[Diagnosis] = db_session.query(Diagnosis).filter_by(patient_id=patient.id).all()
  return diagnosis