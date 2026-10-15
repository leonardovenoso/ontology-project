from sqlalchemy.orm import Session
from tests.helpers.staff_helper import create_admin_staff
from models.staff import Staff
from agent.tools import build_tools

def test_only_doctor_access_to_diagnosis_tools(db_session: Session):
  create_admin_staff(db_session)
  admin_staff = db_session.query(Staff).filter_by(role="admin_staff").one()
  assert build_tools(admin_staff, db_session) == []
