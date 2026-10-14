from sqlalchemy.orm import Session
from models.patient import Patient
from models.diagnosis import Diagnosis
from models.staff import Staff
from tests.helpers.staff_helper import create_doctor_staff, create_pharmacy_staff
from tests.helpers.patients_helper import create_patient
from actions.add_diagnosis_action import add_diagnosis
from schemas.diagnosis_schema import DiagnosisParam
from actions.find_diagnosis_action import find_diagnosis
import pytest

def test_get_patient_diagnosis(db_session: Session):
  create_doctor_staff(db_session)
  doctor = db_session.query(Staff).filter_by(role="doctor").one()

  create_patient(db_session)
  patient = db_session.query(Patient).one()

  diagnosis_1_param = DiagnosisParam(patient_id=patient.id, staff_id=doctor.id, diagnosis="Patient reported stomach ache")
  add_diagnosis(diagnosis_1_param, doctor, db_session)

  diagnosis_2_param = DiagnosisParam(patient_id=patient.id, staff_id=doctor.id, diagnosis="Patient reported bloated belly, and acid reflux after dinner.")
  add_diagnosis(diagnosis_2_param, doctor, db_session)

  diagnosis = find_diagnosis(patient.mrn, doctor, db_session)
  assert diagnosis[0].diagnosis == diagnosis_1_param.diagnosis
  assert diagnosis[1].diagnosis == diagnosis_2_param.diagnosis


def test_get_patient_diagnosis_with_incorrect_role(db_session: Session):
  create_doctor_staff(db_session)
  doctor = db_session.query(Staff).filter_by(role="doctor").one()

  create_patient(db_session)
  patient = db_session.query(Patient).one()

  diagnosis_1_param = DiagnosisParam(patient_id=patient.id, staff_id=doctor.id, diagnosis="Patient reported stomach ache")
  add_diagnosis(diagnosis_1_param, doctor, db_session)

  diagnosis_2_param = DiagnosisParam(patient_id=patient.id, staff_id=doctor.id, diagnosis="Patient reported bloated belly, and acid reflux after dinner.")
  add_diagnosis(diagnosis_2_param, doctor, db_session)

  create_pharmacy_staff(db_session)
  pharmacy = db_session.query(Staff).filter_by(role="pharmacy").one()

  with pytest.raises(PermissionError, match="Invalid role"):
    find_diagnosis(patient.mrn, pharmacy, db_session)
  