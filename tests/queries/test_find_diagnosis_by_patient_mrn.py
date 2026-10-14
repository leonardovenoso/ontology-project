from sqlalchemy.orm import Session
from tests.helpers.patients_helper import create_patient
from tests.helpers.staff_helper import create_doctor_staff
from actions.add_diagnosis_action import add_diagnosis
from schemas.diagnosis_schema import DiagnosisParam
from models.staff import Staff
from models.patient import Patient
from models.diagnosis import Diagnosis
from queries.find_diagnosis_by_patient_mrn import find_diagnosis_by_patient_mrn

def test_find_diagnosis_by_patient_mrn(db_session: Session):
  create_patient(db_session)
  create_doctor_staff(db_session)
  
  doctor = db_session.query(Staff).filter_by(role="doctor").one()
  patient = db_session.query(Patient).one()
  
  diagnosis_1_param = DiagnosisParam(staff_id=doctor.id, patient_id=patient.id, diagnosis="Stomach age and gastric reflux")
  add_diagnosis(param=diagnosis_1_param, caller=doctor, db_session=db_session)

  diagnosis_2_param = DiagnosisParam(staff_id=doctor.id, patient_id=patient.id, diagnosis="Slow digestion and bloating")
  add_diagnosis(param=diagnosis_2_param, caller=doctor, db_session=db_session)

  diagnosis: list[Diagnosis] = find_diagnosis_by_patient_mrn(mrn=patient.mrn, db_session=db_session)

  assert diagnosis[0].diagnosis == diagnosis_1_param.diagnosis
  assert diagnosis[1].diagnosis == diagnosis_2_param.diagnosis