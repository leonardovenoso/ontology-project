from schemas.shift_assignment_schema import AssignShiftParams
from datetime import datetime, time, timedelta
from tests.helpers.staff_helper import create_admin_staff, create_pharmacy_staff
from tests.helpers.sections_helper import create_sections
from models.staff import Staff
from models.section import Section
from models.shift_assignment import ShiftAssignment
from datetime import date, timedelta, time
from actions.shift_assignment_action import assign_shift_to_staff
import pytest
import uuid

def test_assign_shift_to_staff(db_session):
  create_admin_staff(db_session)
  admin_staff = db_session.query(Staff).first()

  create_sections(db_session)
  section = db_session.query(Section).first()

  params = AssignShiftParams(staff_id=admin_staff.id, section_id=section.id, day_from=date.today(), day_to=date.today() + timedelta(days=1), hour_from=time(8, 0), hour_to=time(16, 0))
  assign_shift_to_staff(params, admin_staff, db_session)

  shift_assignment = db_session.query(ShiftAssignment).first()
  assert shift_assignment is not None


def test_try_assign_assignment_with_wrong_staff_role(db_session):
  create_pharmacy_staff(db_session)
  pharmacy_staff = db_session.query(Staff).first()

  create_sections(db_session)
  section = db_session.query(Section).first()

  params = AssignShiftParams(staff_id=pharmacy_staff.id, section_id=section.id, day_from=date.today(), day_to=date.today() + timedelta(days=1), hour_from=time(8, 0), hour_to=time(16, 0))

  with pytest.raises(ValueError, match="Invalid role"):
    assign_shift_to_staff(params, pharmacy_staff, db_session)


def test_try_assign_shift_with_wrong_section_id(db_session):
  create_admin_staff(db_session)
  admin_staff = db_session.query(Staff).first()

  params = AssignShiftParams(staff_id=admin_staff.id, section_id=uuid.uuid4(), day_from=date.today(), day_to=date.today() + timedelta(days=1), hour_from=time(8, 0), hour_to=time(16, 0))

  with pytest.raises(ValueError, match="Invalid section"):
    assign_shift_to_staff(params, admin_staff, db_session)

