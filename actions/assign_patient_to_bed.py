from sqlalchemy.orm import Session
from schemas.occupancy_schema import AssignPatientToBedParams
from models.staff import Staff
from models.occupancy import Occupancy
from models.bed import Bed
from models.patient import Patient
from constants import BedStatus, OccupancyStatus

def assign_patient_to_bed(params:  AssignPatientToBedParams, caller: Staff, db_session: Session):
  if caller.role != "admin_staff":
    raise PermissionError("Invalid role")
  
  bed = db_session.query(Bed).filter_by(id=params.bed_id, status=BedStatus.FREE).one()
  patient = db_session.query(Patient).filter_by(id=params.patient_id).one()

  if params.admission_date >= params.discharge_date:
    raise ValueError("Discharge date must be later than admission date")
  
  occupancy = Occupancy(patient_id=patient.id, bed_id=bed.id, admit_date=params.admission_date, discharge_date=params.discharge_date, status=OccupancyStatus.ACTIVE)
  bed.status = BedStatus.TAKEN

  db_session.add(occupancy)
  db_session.add(bed)

  db_session.commit()
  