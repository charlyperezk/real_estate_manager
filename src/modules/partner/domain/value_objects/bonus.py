from dataclasses import dataclass
from src.seedwork.domain.value_objects import Money
from ..enums.bonus_type import BonusType

@dataclass(frozen=True)
class Bonus:
    type: BonusType
    amount: Money | float