from schemas.occupancy_schema import DischargePatientParams
from models.staff import Staff
from models.occupancy import Occupancy
from sqlalchemy.orm import Session
from constants import OccupancyStatus
from datetime import datetime

def discharge_patient(params: DischargePatientParams, caller: Staff, db_session: Session) -> bool:
  if caller.role != 'admin_staff':
    raise PermissionError('Invalid role')
 
  occupancy = db_session.query(Occupancy).filter_by(patient_id=params.patient_id, status=OccupancyStatus.ACTIVE).order_by(Occupancy.admit_date.desc()).first()
  
  if occupancy == None:
    raise ValueError('Patient was not admitted')

  occupancy.status = OccupancyStatus.DISCHARGED
  occupancy.discharge_date = datetime.now()
  db_session.add(occupancy)
  db_session.commit()
  
  return True