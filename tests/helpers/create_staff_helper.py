from models.staff import Staff

def create_admin_staff(db_session):
  staff_data = {"role": "admin_staff", "first_name": "Christina", "last_name": "Motus"}
  caller = Staff(**staff_data)
  
  db_session.add(caller)
  db_session.commit()