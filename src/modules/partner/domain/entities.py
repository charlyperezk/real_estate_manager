from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from src.seedwork.domain.entities import GenericUUID, AggregateRoot
from .partnership import Partnership, OperationType
from .status import PartnershipStatus
from .types import PartnershipType
from .value_objects.partner_fee import PartnerFee
from .operations import Operation, Operations, AchievementType, OperationStatus
from .events import (
    PartnerFeeAddedToPartnership,
    PartnerFeeUpdated,
    PartnershipWasActivated,
    PartnershipWasFinished,
    PartnerOperationStatusChangedToPaid,
    PartnerOperationStatusChangedToInProgress,
    PartnerOperationStatusChangedToCancelled,
    OperationAddedToPartner,
    OperationDeletedFromPartner
)

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
        # Verificar que no este finalizado el partner
        self.partnership.add_fee(partner_fee)
        self.register_event(
            PartnerFeeAddedToPartnership(
                partner_id=self.id,
                fee=partner_fee
            )
        )

    def update_fee(self, partner_fee: PartnerFee) -> None:
        self.partnership.update_fee(partner_fee)
        self.register_event(
            PartnerFeeUpdated(
                partner_id=self.id,
                fee=partner_fee
            )
        )

    def get_fees(self, operation_type: OperationType) -> List[PartnerFee]:
        return self.partnership.get_fees(type=operation_type)
    
    def activate(self) -> None:
        assert self.status != PartnershipStatus.ACTIVE
        self.status = PartnershipStatus.ACTIVE
        self.register_event(
            PartnershipWasActivated(
                partner_id=self.id,
                user_id=self.user_id,
                type=self.type,
                operations=self.operations
            )
        )

    def finish(self) -> None:
        assert self.status != PartnershipStatus.FINISHED
        self.status = PartnershipStatus.FINISHED
        self.register_event(
            PartnershipWasFinished(
                partner_id=self.id,
                user_id=self.user_id,
                type=self.type,
                operations=self.operations
            )
        )

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
        self.register_event(
            OperationAddedToPartner(
                partner_id=self.id,
                operation=operation
            )
        )

    def _set_operation_status(self, operation_id: GenericUUID, status: OperationStatus) -> None:
        operation = self.get_operation_by_id(operation_id=operation_id)
        assert operation.status != status, "The provided status is already set"

        self.operations.update_operation(
            operation_id=operation_id,
            status=status
        )

    def mark_operation_as_paid(self, operation_id: GenericUUID) -> None:
        self._set_operation_status(operation_id=operation_id, status=OperationStatus.PAID)
        self.register_event(
            PartnerOperationStatusChangedToPaid(
                partner_id=self.id,
                operation=self.get_operation_by_id(operation_id=operation_id)
            )
        )

    def mark_operation_as_in_progress(self, operation_id: GenericUUID) -> None:
        self._set_operation_status(operation_id=operation_id, status=OperationStatus.IN_PROGRESS)
        self.register_event(
            PartnerOperationStatusChangedToInProgress(
                partner_id=self.id,
                operation=self.get_operation_by_id(operation_id=operation_id)
            )
        )

    def cancel_operation(self, operation_id: GenericUUID) -> None:
        self._set_operation_status(operation_id=operation_id, status=OperationStatus.CANCELLED)
        self.register_event(
            PartnerOperationStatusChangedToCancelled(
                partner_id=self.id,
                operation=self.get_operation_by_id(operation_id=operation_id)
            )
        )

    def delete_operation(self, operation_id: GenericUUID) -> None:
        self.operations.delete_operation(operation_id=operation_id)
        self.register_event(
            OperationDeletedFromPartner(
                partner_id=self.id,
                operation=self.get_operation_by_id(operation_id=operation_id)
            )
        )
        