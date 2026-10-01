from schemas.bed_schema import CreateBedParams
import pytest
from pydantic import ValidationError
import uuid

def test_bed_has_all_attributes():
  data = {"section_id": uuid.uuid4(), "status": "taken"}
  params = CreateBedParams(**data)
  
  assert params.section_id == data["section_id"]
  assert params.status == data["status"]


def test_missing_status_raise_an_error():
  with pytest.raises(ValidationError):
    data = {"status": "taken"}
    CreateBedParams(**data) # type: ignore


def test_correct_types():
  with pytest.raises(ValidationError):
    data = {"section_id": uuid.uuid4(), "status": 111}
    CreateBedParams(**data)
