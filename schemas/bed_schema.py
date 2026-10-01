import uuid
from pydantic import BaseModel

class CreateBedParams(BaseModel):
  section_id: uuid.UUID
  status: str