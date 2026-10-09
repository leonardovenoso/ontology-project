from models.bed import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey, String
import uuid

class Diagnosis(BaseModel):
  __tablename__ = "diagnosis"

  staff_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
  patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)  
  diagnosis: Mapped[str] = mapped_column(String(250))
