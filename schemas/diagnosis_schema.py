from pydantic import BaseModel, Field
import uuid

class DiagnosisParam(BaseModel):
  staff_id: uuid.UUID
  mrn: str
  diagnosis: str = Field(min_length=10, max_length=250)