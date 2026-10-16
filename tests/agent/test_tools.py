import pytest
from sqlalchemy.orm import Session
from tests.helpers.staff_helper import create_admin_staff, create_doctor_staff
from models.staff import Staff
from agent.tools import build_tools
from agent.tools import get_diagnosis_list, get_ai_hidden_disease_patterns, get_ai_diagnosis, get_pub_med_citations
from tests.helpers.patients_helper import create_patient
from schemas.diagnosis_schema import DiagnosisParam
from actions.add_diagnosis_action import add_diagnosis
from models.patient import Patient
from agent.tools import DoctorToolsContext
from types import SimpleNamespace
from langchain_core.tools import StructuredTool
from models.diagnosis import Diagnosis

def test_only_doctor_access_to_diagnosis_tools(db_session: Session):
  create_admin_staff(db_session)
  admin_staff = db_session.query(Staff).filter_by(role="admin_staff").one()
  
  with pytest.raises(PermissionError, match="Invalid role"):
    build_tools(admin_staff)


def test_only_doctor_can_access_diagnosis_tools(db_session: Session):
  create_doctor_staff(db_session)
  doctor = db_session.query(Staff).filter_by(role="doctor").one()
  assert build_tools(doctor) == [get_diagnosis_list, get_ai_hidden_disease_patterns, get_ai_diagnosis, get_pub_med_citations]


def test_get_patient_diagnosis(db_session: Session):
  create_patient(db_session)
  create_doctor_staff(db_session)

  doctor = db_session.query(Staff).filter_by(role="doctor").one()
  patient = db_session.query(Patient).first()

  diagnosis_param = DiagnosisParam(staff_id=doctor.id, mrn=patient.mrn, diagnosis="Bloated belly after drinking milk")
  add_diagnosis(param=diagnosis_param, caller=doctor, db_session=db_session)

  doctor_tool_context = DoctorToolsContext(caller=doctor, db_session=db_session, mrn=patient.mrn)
  assert isinstance(get_diagnosis_list, StructuredTool)
  assert get_diagnosis_list.func is not None

  result: list[Diagnosis] = get_diagnosis_list.func(SimpleNamespace(context=doctor_tool_context))
  
  assert diagnosis_param.diagnosis in [res.diagnosis for res in result]