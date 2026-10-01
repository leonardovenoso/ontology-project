import uuid
from datetime import datetime
from schemas.occupancy_schema import AssignPatientToBedParams
from pydantic import ValidationError
import pytest

def test_occupancy_has_all_attriutes():
  data = {"patient_id": uuid.uuid4(), "bed_id": uuid.uuid4(), "admission_date": datetime.now()}
  params = AssignPatientToBedParams(**data)

  assert params.patient_id is not None
  assert params.bed_id is not None
  assert params.admission_date is not None


def test_occupancy_missing_patiend_id():
  data = {"patient_id": None, "bed_id": uuid.uuid4(), "admission_date": datetime.now()}
  with pytest.raises(expected_exception=ValidationError): 
    AssignPatientToBedParams(**data)


def test_occupancy_missing_bed_id():
  data = {"patient_id": None, "bed_id": uuid.uuid4(), "admission_date": datetime.now()}
  with pytest.raises(expected_exception=ValidationError):
    AssignPatientToBedParams(**data)


def test_occupancy_missing_admission_date():
  data = {"patient_id": None, "bed_id": uuid.uuid4(), "admission_date": None}
  with pytest.raises(expected_exception=ValidationError):
    AssignPatientToBedParams(**data)

  