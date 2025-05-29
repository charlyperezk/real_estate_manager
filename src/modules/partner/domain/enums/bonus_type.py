from enum import Enum

class BonusType(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"