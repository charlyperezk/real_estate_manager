from enum import Enum

class OperationType(str, Enum):
    SELL = "sell"
    RENT = "rent"