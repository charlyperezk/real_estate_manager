from datetime import datetime
from typing import Optional, Union
from dataclasses import dataclass, field
from src.seedwork.domain.entities import GenericUUID, AggregateRoot
from .operation_type import OperationType
from .achievement_types import AchievementType
from .status import OperationStatus
from src.seedwork.domain.value_objects import Money, Fee

OWN = "own"

@dataclass
class Operation(AggregateRoot):
    property_id: GenericUUID
    strategy_id: GenericUUID
    operation: OperationType
    fee: Fee
    amount: Money
    achievement: AchievementType
    status: OperationStatus = field(default=OperationStatus.ACTIVE)
    partner_id: Union[str, GenericUUID] = field(default=OWN)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    in_progress_at: Optional[datetime] = field(default=None)
    completed_at: Optional[datetime] = field(default=None)

    def complete(self) -> None:
        assert self.status != OperationStatus.CANCELLED, "You cant mark as complete the operation if the status is cancelled"

        self.in_progress_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = OperationStatus.IN_PROGRESS

    def paid(self) -> None:
        assert self.status != OperationStatus.CANCELLED, "You cant mark as paid the operation if the status is cancelled"
        
        self.updated_at = datetime.now()
        self.completed_at = datetime.now()
        self.status = OperationStatus.PAID
    
    def cancel(self) -> None:
        assert self.status != OperationStatus.CANCELLED, "The operation status is already cancelled"
        self.updated_at = datetime.now()
        self.status = OperationStatus.CANCELLED

    def set_achievement(self, achievement_type: AchievementType) -> None:
        self.updated_at = datetime.now()
        self.achievement = achievement_type

    # def set_bonification_applyed(self, bonification: Bonification)