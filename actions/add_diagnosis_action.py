from schemas.diagnosis_schema import DiagnosisParam
from models.staff import Staff
from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis
from models.patient import Patient

def add_diagnosis(param: DiagnosisParam, caller: Staff, db_session: Session):
  if caller.role != "doctor":
    raise PermissionError("Invalid role")

  db_session.query(Staff).filter_by(id=caller.id).one()
  db_session.query(Patient).filter_by(id=param.patient_id).one()

  diagnosis = Diagnosis(staff_id=caller.id, patient_id=param.patient_id, diagnosis=param.diagnosis)
  db_session.add(diagnosis)
  db_session.commit()