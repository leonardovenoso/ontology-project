import uuid
from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey, DateTime, Time

class ShiftAssignment(BaseModel):
  __tablename__ = "shift_assignments"
  staff_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
  section_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)
  day_from: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
  day_to:  Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
  hour_from: Mapped[Time] = mapped_column(Time, nullable=False)
  hour_to: Mapped[Time]= mapped_column(Time, nullable=False)