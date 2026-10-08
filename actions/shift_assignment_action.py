from schemas.shift_assignment_schema import AssignShiftParams
from models.staff import Staff
from models.shift_assignment import ShiftAssignment
from models.section import Section
from sqlalchemy.orm import Session

def assign_shift_to_staff(params: AssignShiftParams, caller: Staff, db_session: Session):
  if caller.role != "admin_staff":
    raise ValueError("Invalid role")

  section = db_session.query(Section).filter_by(id=params.section_id).first()
  if section is None:
    raise ValueError("Invalid section")

  shift_assignment = ShiftAssignment(staff_id=caller.id, section_id=params.section_id, day_from=params.day_from, day_to=params.day_to, hour_from=params.hour_from, hour_to=params.hour_to)
  db_session.add(shift_assignment)
  db_session.commit()
