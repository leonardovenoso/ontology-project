from sqlalchemy.orm import Session
from tests.helpers.patients_helper import create_patient
from models.patient import Patient
from queries.find_patient_by_mrn import find_patient_by_mrn

def test_find_patient_by_mrn(db_session: Session):
  create_patient(db_session)
  patient = db_session.query(Patient).one()

  patient = find_patient_by_mrn(patient.mrn, db_session)
  assert patient is not None


def test_find_patient_with_unexisting_mrn(db_session: Session):
  create_patient(db_session)
  patient = db_session.query(Patient).one()

  patient = find_patient_by_mrn("9F3A1C2B", db_session)
  assert patient is None