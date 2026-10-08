from schemas.bed_schema import CreateBedParams
from actions.bed_action import create_bed
from actions.discharge_patient_action import discharge_patient
from models.staff import Staff
from tests.helpers.sections_helper import create_sections, get_section_id_by_name
from tests.helpers.staff_helper import create_admin_staff, create_pharmacy_staff
from tests.helpers.patients_helper import create_patient
from constants import BedStatus, OccupancyStatus
from models.patient import Patient
from models.occupancy import Occupancy
from models.bed import Bed
from actions.assign_patient_to_bed_action import assign_patient_to_bed
from schemas.occupancy_schema import AssignPatientToBedParams, DischargePatientParams
from datetime import datetime, timedelta
import pytest

def create_patient_with_bed_assigned(db_session):
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


def test_discharge_patient(db_session):
  create_patient_with_bed_assigned(db_session)

  patient = db_session.query(Patient).first()
  patient_occupancy = db_session.query(Occupancy).filter_by(patient_id=patient.id).first() # Assuming one bed per patient
  params = DischargePatientParams(patient_id=patient_occupancy.patient_id)
  admin_staff_caller = db_session.query(Staff).filter_by(role='admin_staff').first()

  discharge_patient(params, admin_staff_caller, db_session)
  current_patient_occupancy = db_session.query(Occupancy).filter_by(patient_id=patient.id).first() # Assuming one bed per patient
  bed = db_session.query(Bed).filter_by(id=current_patient_occupancy.bed_id).first()

  assert current_patient_occupancy.status == OccupancyStatus.DISCHARGED
  assert bed.status == BedStatus.FREE


def test_try_discharge_an_already_discharged_patient(db_session):
  create_patient_with_bed_assigned(db_session)

  patient = db_session.query(Patient).first()
  patient_occupancy = db_session.query(Occupancy).filter_by(patient_id=patient.id).first() # Assuming one bed per patient
  params = DischargePatientParams(patient_id=patient_occupancy.patient_id)
  admin_staff_caller = db_session.query(Staff).filter_by(role='admin_staff').first()
  discharge_patient(params, admin_staff_caller, db_session)

  with pytest.raises(ValueError, match='Patient was not admitted'):
    discharge_patient(params, admin_staff_caller, db_session)


def test_try_discharge_patient_with_wrong_staff_role(db_session ):
  create_patient_with_bed_assigned(db_session)
  create_pharmacy_staff(db_session)

  patient = db_session.query(Patient).first()
  patient_occupancy = db_session.query(Occupancy).filter_by(patient_id=patient.id).first() # Assuming one bed per patient
  params = DischargePatientParams(patient_id=patient_occupancy.patient_id)
  pharmacy_staff_caller = db_session.query(Staff).filter_by(role='pharmacy').first()

  with pytest.raises(PermissionError, match='Invalid role'):
    discharge_patient(params, pharmacy_staff_caller, db_session)


def test_try_discharge_patient_that_was_never_admitted(db_session):
  create_admin_staff(db_session)
  admin_staff_caller = db_session.query(Staff).first()

  create_patient(db_session)
  patient = db_session.query(Patient).first()

  params = DischargePatientParams(patient_id=patient.id)

  with pytest.raises(ValueError, match='Patient was not admitted'):
    discharge_patient(params, admin_staff_caller, db_session)


def test_try_to_free_bed_with_wrong_bed_id(db_session):
  create_patient_with_bed_assigned(db_session)

  patient = db_session.query(Patient).first()
  patient_occupancy = db_session.query(Occupancy).filter_by(patient_id=patient.id).first()
  params = DischargePatientParams(patient_id=patient_occupancy.patient_id)
  admin_staff_caller = db_session.query(Staff).filter_by(role='admin_staff').first()

  bed = db_session.query(Bed).first()
  db_session.delete(bed)
  db_session.commit()

  with pytest.raises(ValueError, match='Bed not found'):
    discharge_patient(params, admin_staff_caller, db_session)
