import uuid
from pydantic import BaseModel
from datetime import date

class EquipmentParams(BaseModel):
  name: str
  section_id: uuid.UUID
  maintenance_date: date