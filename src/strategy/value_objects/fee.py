from __future__ import annotations
from dataclasses import dataclass
from ...seedwork.domain.value_objects import ValueObject

@dataclass(frozen=True)
class Fee(ValueObject):
    value: float

    def __post_init__(self):
        assert self.value > 0, "Fee value must be greather than 0"

class SellFee(Fee):
    value = 6

class RentFee(Fee):
    value = 100