from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from models.base import BaseModel

class Section(BaseModel):
  __tablename__ = "sections"

  name: Mapped[str] = mapped_column(String, nullable=False, unique=True)