from __future__ import annotations
from enum import Enum
from dataclasses import dataclass

class SuperficeUnity(Enum):
    M2 = "m2"

@dataclass
class Superfice:
    value: float
    unity: SuperficeUnity

    def __post_init__(self):
        assert self.value > 0, "Superfice value must be greather than zero"

    def __lt__(self, superfice: Superfice) -> bool:
        #TODO: add case when superfice to compare has another unity
        return self.value < superfice.value
    
    def __gt__(self, superfice: Superfice) -> bool:
        #TODO: add case when superfice to compare has another unity
        return self.value > superfice.value