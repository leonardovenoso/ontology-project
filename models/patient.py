from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Patient (BaseModel):
  __tablename__ = "patients"

  first_name: Mapped[str] = mapped_column(String, nullable=False)
  last_name: Mapped[str] = mapped_column(String, nullable=False)
  passport_number: Mapped[str] = mapped_column(String, nullable=False)
  country: Mapped[str] = mapped_column(String, nullable=False)
