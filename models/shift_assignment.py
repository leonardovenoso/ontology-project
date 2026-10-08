import uuid
from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey, DateTime, Time
from datetime import datetime, time

class ShiftAssignment(BaseModel):
  __tablename__ = "shift_assignments"
  staff_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
  section_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)
  day_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  day_to: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  hour_from: Mapped[time] = mapped_column(Time, nullable=False)
  hour_to: Mapped[time] = mapped_column(Time, nullable=False)


  