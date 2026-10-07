from pydantic import BaseModel
import uuid
from datetime import datetime

class AssignPatientToBedParams(BaseModel):
  patient_id: uuid.UUID
  bed_id: uuid.UUID
  admission_date: datetime
  discharge_date: datetime

class DischargePatientParams(BaseModel):
  patient_id: uuid.UUID