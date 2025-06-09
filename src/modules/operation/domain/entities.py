from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Callable, Any
from dataclasses import dataclass, field
from src.seedwork.domain.entities import GenericUUID, AggregateRoot
from src.seedwork.domain.value_objects import Money, Fee, Period
from ...shared_kernel import OperationType
from ...shared_kernel.achievement_types import AchievementType
from .operation_status import OperationStatus
from .rules import (
    OperationMustNotBeUnderReview,
    OperationMustNotBeCancelled,
    AchievementTypeMustChange
)
from .events import (
    OperationStatusChangedToInProgress
)
from .exceptions import ConsistencyError

@dataclass
class Operation(AggregateRoot):
    property_id: GenericUUID
    strategy_id: GenericUUID
    partner_id: GenericUUID
    achievement_type: AchievementType
    type: OperationType
    fee: Fee
    amount: Money
    description: str
    status: OperationStatus = field(default=OperationStatus.ACTIVE)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    in_progress_at: Optional[datetime] = field(default=None)
    completed_at: Optional[datetime] = field(default=None)

    @property
    def must_impact(self) -> bool:
        return self.status in [OperationStatus.ACTIVE, OperationStatus.IN_PROGRESS, OperationStatus.PAID]

    def in_progress(self) -> None:
        self.check_rule(OperationMustNotBeCancelled(status=self.status))
        now = datetime.now()

        self.in_progress_at = now
        self.updated_at = now
        self.status = OperationStatus.IN_PROGRESS

        self.register_event(
            OperationStatusChangedToInProgress(
                partner_id=self.partner_id,
                achievement_type=self.achievement_type,
                revenue=self.amount,
                fee=self.fee,
                period=Period(year=now.year, month=now.month)
            )
        )

    def paid(self) -> None:
        self.check_rule(OperationMustNotBeCancelled(status=self.status))
        now = datetime.now()

        self.updated_at = now
        self.completed_at = now
        self.status = OperationStatus.PAID
    
    def under_review(self) -> None:
        self.check_rule(OperationMustNotBeUnderReview(status=self.status))
        
        self.updated_at = datetime.now()
        self.status = OperationStatus.UNDER_REVIEW

    def cancel(self) -> None:
        self.check_rule(OperationMustNotBeCancelled(status=self.status))
        
        self.updated_at = datetime.now()
        self.status = OperationStatus.CANCELLED

    def set_achievement(self, achievement_type: AchievementType) -> None:
        self.check_rule(
            AchievementTypeMustChange(
                achievement_type=achievement_type,
                actual_achievement_type=self.achievement_type
            )
        )
        
        self.updated_at = datetime.now()
        self.achievement_type = achievement_type

    def set_fraction(self, revenue: Money, fee: Fee) -> None:
        self.amount = revenue
        self.fee = fee

@dataclass
class RealEstateOperation:
    strategy_id: GenericUUID
    property_id: GenericUUID
    type: OperationType
    management: Operation
    capture: Optional[Operation] = None
    close: Optional[Operation] = None

    @property
    def fullfilled(self) -> bool:
        return bool(self.management and self.capture and self.close)

    @property
    def operations(self) -> List[Operation]:
        return [op for op in (self.management, self.close, self.capture) if op and op.must_impact]

    @property
    def completed(self) -> bool:
        return all((op.status == OperationStatus.PAID for op in self.operations)) and self.fullfilled

    @property
    def revenue(self) -> Money:
        return self.management.amount

    @property
    def fee(self) -> Fee:
        return self.management.fee

    @property
    def broker_fee(self) -> Fee:
        impactables = [op for op in self.operations if op.achievement_type != AchievementType.MANAGEMENT]
        if any(impactables):
            fee = sum([fraction.fee for fraction in impactables if fraction])# type: ignore
            return self.calculate_management_fee_substracting_partner_tier(tier_partner=fee)
        else:
            return self.management.fee

    @property
    def broker_revenue(self) -> Money:
        from functools import reduce

        impactables = [op for op in self.operations if op.achievement_type != AchievementType.MANAGEMENT]
        if any(impactables):
            partner_revenues = sum([fraction.amount for fraction in impactables if fraction])# type: ignore
            return reduce(
                lambda revenue, partner_revenue: revenue - partner_revenue.amount,
                partner_revenues,
                self.management.amount
            )
        else:
            return self.management.amount

    def calculate_management_fee_substracting_partner_tier(self, tier_partner: Fee) -> Fee:
        return Fee(
            value=(self.management.fee.value * (100 - tier_partner.value)) / 100
        )

    def calculate_partner_revenue(self, tier_partner: Fee) -> Money:
        revenue_partner = (self.management.amount * tier_partner.value) / 100
        return revenue_partner
    
    def set_capture(self, operation: Operation):
        if operation.achievement_type != AchievementType.CAPTURE:
            raise ConsistencyError.operation_with_wrong_achievement_type_received(
                desired_achievement_type=AchievementType.CAPTURE
            )

        if self.capture and self.capture.must_impact:
            raise ConsistencyError.valid_achievement_operation_already_setted(
                achievement_type=operation.achievement_type
            )

        self.capture = operation

    def set_close(self, operation: Operation):
        if operation.achievement_type != AchievementType.CLOSE:
            raise ConsistencyError.operation_with_wrong_achievement_type_received(
                desired_achievement_type=AchievementType.CLOSE
            )

        if self.capture and self.capture.must_impact:
            raise ConsistencyError.valid_achievement_operation_already_setted(
                achievement_type=operation.achievement_type
            )

        self.close = operation

    def map_operations(self, func: Callable[[Operation], Any]) -> List[Any]:
        return [func(op) for op in self.operations]

    def under_review(self) -> None:        
        for op in self.operations:
            op.under_review()
    
    def in_progress(self) -> None:
        for op in self.operations:
            op.in_progress()

    @classmethod
    def from_operations(cls, operations: List[Operation]) -> RealEstateOperation:
        management = next((op for op in operations if op.achievement_type == AchievementType.MANAGEMENT), None)
        if not management:
            raise ConsistencyError.management_operation_not_found()
        
        re_operation = cls(
            property_id=management.property_id,
            strategy_id=management.strategy_id,
            type=management.type,
            management=management
        )

        others = [op for op in operations if op.achievement_type != AchievementType.MANAGEMENT]
        if not all([op.strategy_id == management.strategy_id for op in others]):
            raise ConsistencyError.foreign_operations_found()
        
        if any(others):
            for op in others:
                if op.achievement_type == AchievementType.CLOSE:
                    if not re_operation.close or re_operation.close and not re_operation.close.must_impact:
                        re_operation.set_close(operation=op)

                elif op.achievement_type == AchievementType.CAPTURE:
                    if not re_operation.capture or re_operation.capture and not re_operation.capture.must_impact:
                        re_operation.set_capture(operation=op)

        return re_operation