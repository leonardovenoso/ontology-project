import uuid
from pydantic import BaseModel
from constants import BedStatus

class CreateBedParams(BaseModel):
  section_id: uuid.UUID
  status: BedStatus
