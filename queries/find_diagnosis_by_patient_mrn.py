from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis
from models.patient import Patient

def find_diagnosis_by_patient_mrn(mrn: str, db_session: Session) -> list[Diagnosis]:
  patient = db_session.query(Patient).filter_by(mrn=mrn).first()
  
  if patient is None:
    return []

  diagnosis: list[Diagnosis] = db_session.query(Diagnosis).filter_by(patient_id=patient.id).all()
  return diagnosis