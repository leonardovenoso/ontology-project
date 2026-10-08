import uuid
from datetime import date, time
from pydantic import BaseModel

class AssignShiftParams(BaseModel):
  staff_id: uuid.UUID
  section_id: uuid.UUID
  day_from: date
  day_to: date
  hour_from: time
  hour_to: time
