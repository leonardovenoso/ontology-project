from sqlalchemy.orm import Session
from tests.helpers.staff_helper import create_doctor_staff, create_admin_staff
from tests.helpers.patients_helper import create_patient
from actions.add_diagnosis_action import add_diagnosis
from schemas.diagnosis_schema import DiagnosisParam
from models.patient import Patient
from models.staff import Staff
from models.diagnosis import Diagnosis
import pytest
from pydantic import ValidationError
import uuid
from sqlalchemy.exc import NoResultFound

def test_add_diagnosis(db_session: Session):
  create_doctor_staff(db_session)
  create_patient(db_session)
  doctor_staff = db_session.query(Staff).filter_by(role="doctor").one()
  patient = db_session.query(Patient).one()

  param = DiagnosisParam(staff_id=doctor_staff.id, mrn=patient.mrn, diagnosis="Medical diagnosis...")
  add_diagnosis(param, doctor_staff, db_session)
  
  diagnosis = db_session.query(Diagnosis).one()
  assert diagnosis.diagnosis == param.diagnosis


def test_add_diagnosis_by_unauthorized_staff(db_session: Session):
  create_admin_staff(db_session)
  create_doctor_staff(db_session)
  create_patient(db_session)
  admin_staff = db_session.query(Staff).filter_by(role="admin_staff").one()
  patient = db_session.query(Patient).one()

  param = DiagnosisParam(staff_id=admin_staff.id, mrn=patient.mrn, diagnosis="Medical diagnosis...")
  
  with pytest.raises(PermissionError, match="Invalid role"):
    add_diagnosis(param, admin_staff, db_session)


def test_add_diagnosis_is_too_short():  
  with pytest.raises(ValidationError, match="should have at least 10 characters"):
    DiagnosisParam(staff_id=uuid.uuid4(), mrn="9F3A1C2B", diagnosis=".........")


def test_add_diagnosis_is_too_long():  
  with pytest.raises(ValidationError, match="at most 250 characters"):
    DiagnosisParam(staff_id=uuid.uuid4(), mrn="9F3A1C2B", diagnosis="." * 251)


def test_add_diagnosis_with_wrong_doctor_id(db_session: Session):
  create_patient(db_session)
  create_doctor_staff(db_session)
  patient = db_session.query(Patient).one()
  doctor_staff = db_session.query(Staff).filter_by(role="doctor").one()

  param = DiagnosisParam(staff_id=uuid.uuid4(), mrn=patient.mrn, diagnosis="Medical diagnosis...")
  db_session.delete(doctor_staff)
  db_session.commit()

  with pytest.raises(NoResultFound):
    add_diagnosis(param, doctor_staff, db_session)


def test_add_diagnosis_with_wrong_mrn(db_session: Session):
  create_patient(db_session)
  create_doctor_staff(db_session)
  patient = db_session.query(Patient).one()
  doctor_staff = db_session.query(Staff).filter_by(role="doctor").one()

  param = DiagnosisParam(staff_id=doctor_staff.id, mrn="9F3A1C2B", diagnosis="Medical diagnosis...")
  db_session.commit()

  with pytest.raises(NoResultFound):
    add_diagnosis(param, doctor_staff, db_session)
