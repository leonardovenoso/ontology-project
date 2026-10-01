from schemas.bed_schema import CreateBedParams
from sqlalchemy.orm import Session
from models.staff import Staff
from models.bed import Bed
from models.section import Section

def create_bed(params: CreateBedParams, caller: Staff, session: Session):  
  if caller.role != "admin_staff":
    raise PermissionError('Invalid role')

  section = session.query(Section).filter_by(id=params.section_id).one()
  bed = Bed(section_id=section.id, status=params.status)

  session.add(bed)
  session.commit()

  return bed
