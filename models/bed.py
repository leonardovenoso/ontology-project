import uuid
from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID, ForeignKey

class Bed(BaseModel):
  __tablename__ = "bed"
  section_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sections.id"), nullable=False)
  status: Mapped[str] = mapped_column(String, nullable=False)