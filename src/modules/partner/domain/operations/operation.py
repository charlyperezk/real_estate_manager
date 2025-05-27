from dataclasses import dataclass
from src.seedwork.domain.entities import Entity
from src.seedwork.domain.value_objects import Fee, Money
from ....shared_kernel.achievement_types import AchievementType
from ....shared_kernel.status import OperationStatus

@dataclass
class Operation(Entity):
    fee: Fee
    amount: Money
    achievement_type: AchievementType
    status: OperationStatus