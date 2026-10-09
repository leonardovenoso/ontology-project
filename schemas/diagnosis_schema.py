from pydantic import BaseModel, Field
import uuid

class DiagnosisParam(BaseModel):
  staff_id: uuid.UUID
  patient_id: uuid.UUID
  diagnosis: str = Field(min_length=10, max_length=250)