from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Staff(BaseModel):
  __tablename__ = "staff"
  
  first_name: Mapped[str] = mapped_column(String, nullable=False)
  last_name: Mapped[str] = mapped_column(String, nullable=False)
  role : Mapped[str] = mapped_column(String, nullable=False)