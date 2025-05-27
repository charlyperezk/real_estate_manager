from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from src.seedwork.domain.entities import GenericUUID, AggregateRoot
from .partnership import Partnership, OperationType
from .status import PartnershipStatus
from .types import PartnershipType
from .value_objects.partner_fee import PartnerFee
from .operations import Operation, Operations, AchievementType, OperationStatus

@dataclass
class Partner(AggregateRoot):
    name: str
    user_id: GenericUUID
    type: PartnershipType
    partnership: Partnership
    status: PartnershipStatus = field(default=PartnershipStatus.ACTIVE)
    operations: Operations = field(default_factory=Operations)
    created_at: datetime = field(default_factory=datetime.now)

    def add_fee(self, partner_fee: PartnerFee) -> None:
        self.partnership.add_fee(partner_fee)

    def update_fee(self, partner_fee: PartnerFee) -> None:
        self.partnership.update_fee(partner_fee)

    def delete_fee(self, operation_type: OperationType) -> None:
        self.partnership.delete_fee(operation_type)

    def get_fees(self, operation_type: OperationType) -> List[PartnerFee]:
        return self.partnership.get_fees(type=operation_type)
    
    def set_status(self, status: PartnershipStatus) -> None:
        self.status = status

    def get_operations(
            self,
            status: Optional[OperationStatus]=None,
            achievement_type: Optional[AchievementType]=None
    ) -> List[Operation]:
        return self.operations.get_operations(status=status, achievement_type=achievement_type)
    
    def get_operation_by_id(self, operation_id: GenericUUID) -> Operation:
        return self.operations.get_operation_by_id(operation_id=operation_id)
    
    def add_operation(self, operation: Operation) -> None:
        self.operations.register_operation(operation=operation)

    def delete_operation(self, operation_id: GenericUUID) -> None:
        self.operations.delete_operation(operation_id=operation_id)