from __future__ import annotations
from enum import Enum

class StrategyStatus(str, Enum):
    ACTIVE = "active"
    DEFEATED = "defeated"
    DISCONTINUED = "discontinued"
    PLANNED = "planned"
    PAUSED = "paused"