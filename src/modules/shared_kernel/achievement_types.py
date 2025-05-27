from enum import Enum

class AchievementType(str, Enum):
    MANAGEMENT = "management"
    CAPTURE = "capture"
    CLOSE = "close"