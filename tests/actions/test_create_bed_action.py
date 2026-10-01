from schemas.bed_schema import CreateBedParams
from actions.bed_action import create_bed
from models.staff import Staff
from tests.helpers.sections_helper import create_sections, get_section_id_by_name
from tests.helpers.create_staff_helper import create_admin_staff, create_pharmacy_staff
import pytest
import uuid
from sqlalchemy.orm.exc import NoResultFound
from constants import BedStatus

def test_create_bed(db_session):
  create_sections(db_session)
  section_id = get_section_id_by_name("pediatry", db_session)

  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).first()
  
  bed_data = {"section_id": section_id, "status": BedStatus.FREE}
  bed_params = CreateBedParams(**bed_data)

  bed = create_bed(bed_params, admin_staff_caller, db_session)

  assert bed.id is not None
  assert bed.section_id is not None
  assert bed.status == BedStatus.FREE


def test_create_bed_by_unauthorized_staff(db_session):
  create_sections(db_session)
  section_id = get_section_id_by_name("pediatry", db_session)
  
  create_pharmacy_staff(db_session)
  pharmacy_staff_caller = db_session.query(Staff).filter_by(role='pharmacy').first()

  bed_data = {"section_id": section_id, "status": BedStatus.FREE}
  bed_params = CreateBedParams(**bed_data)

  with pytest.raises(PermissionError, match='Invalid role'):
    create_bed(bed_params, pharmacy_staff_caller, db_session)
  

def test_valid_section_id(db_session):
  create_sections(db_session)
  create_admin_staff(db_session)

  pharmacy_staff_caller = db_session.query(Staff).filter_by(role='admin_staff').first()

  bed_data = {"section_id": uuid.uuid4(), "status": BedStatus.FREE}
  bed_params = CreateBedParams(**bed_data)

  with pytest.raises(NoResultFound):
    create_bed(bed_params, pharmacy_staff_caller, db_session)
  