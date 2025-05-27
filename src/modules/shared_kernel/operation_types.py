from __future__ import annotations
from typing import List
from enum import Enum

class OperationType(str, Enum):
    RENT = "rent"
    SELL = "sell"

    @staticmethod
    def get_default_types() -> List[str]:
        return [value.value for value in list(OperationType)]