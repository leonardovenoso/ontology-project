from schemas.bed_schema import CreateBedParams
from actions.bed_action import create_bed
from models.staff import Staff
from tests.helpers.sections_helper import create_sections, get_section_id_by_name
from tests.helpers.staff_helper import create_admin_staff, create_pharmacy_staff
from tests.helpers.patients_helper import create_patient
from constants import BedStatus
from models.patient import Patient
from actions.assign_patient_to_bed_action import assign_patient_to_bed
from schemas.occupancy_schema import AssignPatientToBedParams
from datetime import datetime, timedelta
from models.occupancy import Occupancy
from models.bed import Bed
import pytest
import uuid

def test_assign_patient_to_bed(db_session):
  create_sections(db_session)
  section_id = get_section_id_by_name("pediatry", db_session)

  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).first()

  create_patient(db_session)
  patient = db_session.query(Patient).first()

  bed_data = {"section_id": section_id, "status": BedStatus.FREE}
  bed_params = CreateBedParams(**bed_data)
  bed = create_bed(bed_params, admin_staff_caller, db_session)

  assign_patient_params_data = {"patient_id": patient.id, "bed_id": bed.id, "admission_date": datetime.now(), "discharge_date": datetime.now() + timedelta(days=10)}
  assign_patients_to_bed_params = AssignPatientToBedParams(**assign_patient_params_data)
  assign_patient_to_bed(assign_patients_to_bed_params, admin_staff_caller, db_session)

  occupancy = db_session.query(Occupancy).first()
  assert occupancy.id is not None

  bed = db_session.query(Bed).first()
  assert bed.status == BedStatus.TAKEN


def test_assign_a_wrong_patient_id(db_session):
  create_sections(db_session)
  section_id = get_section_id_by_name("pediatry", db_session)

  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).first()

  bed_data = {"section_id": section_id, "status": BedStatus.FREE}
  bed_params = CreateBedParams(**bed_data)
  bed = create_bed(bed_params, admin_staff_caller, db_session)

  assign_patient_params_data = {"patient_id": uuid.uuid4(), "bed_id": bed.id, "admission_date": datetime.now(), "discharge_date": datetime.now() + timedelta(days=10)}
  assign_patients_to_bed_params = AssignPatientToBedParams(**assign_patient_params_data)

  with pytest.raises(Exception):
    assign_patient_to_bed(assign_patients_to_bed_params, admin_staff_caller, db_session)


def test_assign_wrong_bed_id(db_session):
  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).first()

  create_patient(db_session)
  patient = db_session.query(Patient).first()

  assign_patient_params_data = {"patient_id": patient.id, "bed_id": uuid.uuid4(), "admission_date": datetime.now(), "discharge_date": datetime.now() + timedelta(days=10)}
  assign_patients_to_bed_params = AssignPatientToBedParams(**assign_patient_params_data)

  with pytest.raises(Exception):
    assign_patient_to_bed(assign_patients_to_bed_params, admin_staff_caller, db_session)


def test_incorrect_role_cannot_assign_patient_to_bed(db_session):
  create_sections(db_session)
  section_id = get_section_id_by_name("pediatry", db_session)

  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).filter_by(role='admin_staff').first()

  create_pharmacy_staff(db_session)
  pharmacy_staff_caller = db_session.query(Staff).filter_by(role='pharmacy').first()

  create_patient(db_session)
  patient = db_session.query(Patient).first()

  bed_data = {"section_id": section_id, "status": BedStatus.FREE}
  bed_params = CreateBedParams(**bed_data)
  bed = create_bed(bed_params, admin_staff_caller, db_session)

  assign_patient_params_data = {"patient_id": patient.id, "bed_id": bed.id, "admission_date": datetime.now(), "discharge_date": datetime.now() + timedelta(days=10)}
  assign_patients_to_bed_params = AssignPatientToBedParams(**assign_patient_params_data)

  with pytest.raises(PermissionError, match='Invalid role'):
    assign_patient_to_bed(assign_patients_to_bed_params, pharmacy_staff_caller, db_session)


def test_assign_patient_to_taken_bed(db_session):
  create_sections(db_session)
  section_id = get_section_id_by_name("pediatry", db_session)

  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).first()

  create_patient(db_session)
  patient = db_session.query(Patient).first()

  bed_data = {"section_id": section_id, "status": BedStatus.TAKEN}
  bed_params = CreateBedParams(**bed_data)
  bed = create_bed(bed_params, admin_staff_caller, db_session)

  assign_patient_params_data = {"patient_id": patient.id, "bed_id": bed.id, "admission_date": datetime.now(), "discharge_date": datetime.now() + timedelta(days=10)}
  assign_patients_to_bed_params = AssignPatientToBedParams(**assign_patient_params_data)

  with pytest.raises(Exception):
    assign_patient_to_bed(assign_patients_to_bed_params, admin_staff_caller, db_session)


def test_assign_patient_with_same_admission_and_discharge_dates(db_session):
  create_sections(db_session)
  section_id = get_section_id_by_name("pediatry", db_session)

  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).first()

  create_patient(db_session)
  patient = db_session.query(Patient).first()

  bed_data = {"section_id": section_id, "status": BedStatus.FREE}
  bed_params = CreateBedParams(**bed_data)
  bed = create_bed(bed_params, admin_staff_caller, db_session)

  date = datetime.now()
  assign_patient_params_data = {"patient_id": patient.id, "bed_id": bed.id, "admission_date": date, "discharge_date": date}
  assign_patients_to_bed_params = AssignPatientToBedParams(**assign_patient_params_data)

  with pytest.raises(ValueError, match="Discharge date must be later than admission date"):
    assign_patient_to_bed(assign_patients_to_bed_params, admin_staff_caller, db_session)
