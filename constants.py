from enum import Enum

class BedStatus(str, Enum):
    FREE = "free"
    TAKEN = "taken"
    MAINTENANCE = "maintenance"

class OccupancyStatus(str, Enum):
    ACTIVE='active'
    DISCHARGED='discharged'