from pydantic import BaseModel

class CreateBedParams(BaseModel):
    section_name: str
    status: str