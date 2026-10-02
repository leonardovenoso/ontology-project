from models.patient import Patient

def create_patient(db_session):
  data = {"first_name": "Leonardo", "last_name": "Venoso", "passport_number": "AA123456", "country": "SG"}
  patient = Patient(**data)

  db_session.add(patient)
  db_session.commit()