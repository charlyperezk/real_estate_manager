from enum import Enum

class PartnershipStatus(str, Enum):
    ACTIVE = "active"
    PENDENT = "pendent"
    FINISHED = "finished"