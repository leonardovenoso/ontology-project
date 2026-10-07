from sqlalchemy.orm import Session
from schemas.equipment_schema import EquipmentParams
from tests.helpers.staff_helper import create_pharmacy_staff, create_admin_staff
from tests.helpers.sections_helper import create_sections
from models.section import Section
from models.equipment import Equipment
from models.staff import Staff
from actions.equipment_action import create_equipment
from datetime import date
import pytest
import uuid

def test_create_equipment(db_session: Session):
  create_admin_staff(db_session)
  admin_staff = db_session.query(Staff).filter_by(role="admin_staff").first()

  create_sections(db_session)
  section = db_session.query(Section).first()
  
  param = EquipmentParams(name="Endoscope", section_id=section.id, maintenance_date=date.today())
  create_equipment(param, admin_staff, db_session)

  equipment = db_session.query(Equipment).filter_by(name="Endoscope").first()
  assert equipment is not None

def test_try_create_equipment_with_incorrect_role(db_session: Session):
  create_pharmacy_staff(db_session)
  pharmacy_staff = db_session.query(Staff).filter_by(role="pharmacy").first()

  create_sections(db_session)
  section = db_session.query(Section).first()
  
  param = EquipmentParams(name="Endoscope", section_id=section.id, maintenance_date=date.today())
  
  with pytest.raises(PermissionError, match="Invalid role"):
    create_equipment(param, pharmacy_staff, db_session)

def test_try_create_equipment_with_wrong_section_id(db_session: Session):
  create_admin_staff(db_session)
  admin_staff = db_session.query(Staff).filter_by(role="admin_staff").first()
  
  param = EquipmentParams(name="Endoscope", section_id=uuid.uuid4(), maintenance_date=date.today())
  
  with pytest.raises(ValueError, match="Invalid section"):
    create_equipment(param, admin_staff, db_session)

def test_try_create_equipment_without_maintenance_date(db_session: Session):
  return False