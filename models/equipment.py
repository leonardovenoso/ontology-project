from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, UUID, ForeignKey
import uuid

class Equipment(BaseModel):
  __tablename__ = "equipment"

  name: Mapped[str] = mapped_column(String, nullable=False)
  section_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sections.id"), nullable=False)
  maintenance_date: Mapped[str] = mapped_column(Date, nullable=False)