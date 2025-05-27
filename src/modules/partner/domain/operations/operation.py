from datetime import datetime
from dataclasses import dataclass
from src.seedwork.domain.entities import Entity
from src.seedwork.domain.value_objects import Fee, Money, GenericUUID
from ....shared_kernel.achievement_types import AchievementType
from ....shared_kernel.operation_types import OperationType
from ....shared_kernel.status import OperationStatus

@dataclass
class PartnerOperation(Entity):
    fee: Fee
    amount: Money
    strategy_id: GenericUUID
    type: OperationType
    achievement_type: AchievementType
    status: OperationStatus
    created_at: datetime