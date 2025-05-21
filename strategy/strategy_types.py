from __future__ import annotations
from enum import Enum

class StrategyType(str, Enum):
    RENT = "rent"
    SELL = "sell"