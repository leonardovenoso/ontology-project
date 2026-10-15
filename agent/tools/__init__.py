from sqlalchemy.orm import Session
from models.staff import Staff

def build_tools(caller: Staff, db_session: Session):
  return []