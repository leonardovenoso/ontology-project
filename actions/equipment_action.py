from schemas.equipment_schema import EquipmentParams
from models.staff import Staff
from models.equipment import Equipment
from models.section import Section
from sqlalchemy.orm import Session

def create_equipment(params: EquipmentParams, caller: Staff, db_session: Session):
  if caller.role != "admin_staff":
    raise PermissionError("Invalid role")

  section = db_session.query(Section).filter_by(id=params.section_id).first()
  if section == None:
    raise ValueError("Invalid section")

  equipment = Equipment(name=params.name, section_id=section.id, maintenance_date=params.maintenance_date)
  db_session.add(equipment)
  db_session.commit()
  
  return True