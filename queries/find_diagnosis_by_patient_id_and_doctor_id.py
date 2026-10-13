from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis
from uuid import UUID

def find_diagnosis_by_patient_id_and_doctor_id(patient_id: UUID, doctor_id: UUID, db_session: Session) -> list[Diagnosis]:
  diagnosis: list[Diagnosis] = db_session.query(Diagnosis).filter_by(staff_id=doctor_id, patient_id=patient_id).all()
  return diagnosis