from models.staff import Staff

def create_admin_staff(db_session):
  staff_data = {"role": "admin_staff", "first_name": "Christina", "last_name": "Motus"}
  caller = Staff(**staff_data)
  
  db_session.add(caller)
  db_session.commit()

def create_pharmacy_staff(db_session):
  staff_data = {"role": "pharmacy", "first_name": "Rose", "last_name": "Larsson"}
  caller = Staff(**staff_data)
  
  db_session.add(caller)
  db_session.commit()


def create_doctor_staff(db_session):
  staff_data = {"role": "doctor", "first_name": "Gregory", "last_name": "House"}
  caller = Staff(**staff_data)
  
  db_session.add(caller)
  db_session.commit()
