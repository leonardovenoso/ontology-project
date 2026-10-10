from sqlalchemy.orm import Session
from models.patient import Patient

def find_patient_by_mrn(mrn: str, db_session: Session)-> Patient | None :
  return db_session.query(Patient).filter_by(mrn=mrn).one_or_none()
