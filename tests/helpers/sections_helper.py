
from models.section import Section

def create_sections(db_session):
  pneumology = Section(name="pneumology")
  pediatry = Section(name="pediatry")
  gynecology = Section(name="gynecology")

  db_session.add(pneumology)
  db_session.add(pediatry)
  db_session.add(gynecology)
  db_session.commit()
  
def get_section_id_by_name(section_name: str, db_session):
  section = db_session.query(Section).filter_by(name=section_name).first()

  if section:
    return section.id  