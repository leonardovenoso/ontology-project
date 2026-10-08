from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, UUID, ForeignKey
import uuid
from datetime import date

class Equipment(BaseModel):
  __tablename__ = "equipment"

  name: Mapped[str] = mapped_column(String, nullable=False)
  section_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sections.id"), nullable=False)
  maintenance_date: Mapped[date] = mapped_column(Date, nullable=False)