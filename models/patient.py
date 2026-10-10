from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
import secrets

def generate_mrn() -> str:
    return secrets.token_hex(4).upper() # For example: 9F3A1C2B

class Patient (BaseModel):
  __tablename__ = "patients"

  first_name: Mapped[str] = mapped_column(String, nullable=False)
  last_name: Mapped[str] = mapped_column(String, nullable=False)
  passport_number: Mapped[str] = mapped_column(String, nullable=False)
  country: Mapped[str] = mapped_column(String, nullable=False)
  mrn: Mapped[str] = mapped_column(String, nullable=False, unique=True, default=generate_mrn)
