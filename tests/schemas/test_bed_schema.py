from schemas.bed_schema import CreateBedParams
import pytest
from pydantic import ValidationError

def test_bed_has_all_attributes():
  data = {"section_name": "A&E", "status": "taken"}
  params = CreateBedParams(**data)
  
  assert params.section_name == data["section_name"]
  assert params.status == data["status"]


def test_missing_status_raise_an_error():
  with pytest.raises(ValidationError):
    data = {"status": "taken"}
    CreateBedParams(**data)


def test_correct_types():
  with pytest.raises(ValidationError):
    data = {"section_name": 111, "status": 111}
    CreateBedParams(**data) # type: ignore
