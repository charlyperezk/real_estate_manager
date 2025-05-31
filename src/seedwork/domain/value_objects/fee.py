from __future__ import annotations
from dataclasses import dataclass
from .value_objects import ValueObject

@dataclass(frozen=True)
class Fee(ValueObject):
    value: float

    def __post_init__(self):
        assert self.value > 0, "Fee value must be greather than 0"

    def __add__(self, value: Fee) -> Fee:
        return Fee(value=self.value + value.value)
    
    def __sub__(self, value: Fee) -> Fee:
        return Fee(value=self.value - value.value)