from __future__ import annotations
from typing import List
from enum import Enum

class StrategyStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    DISCONTINUED = "discontinued"
    PLANNED = "planned"
    PAUSED = "paused"

    @staticmethod
    def get_default_strategy_status() -> List[str]:
        return [value.value for value in list(StrategyStatus)]