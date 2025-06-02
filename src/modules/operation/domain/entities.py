from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from src.seedwork.domain.entities import GenericUUID, AggregateRoot
from src.seedwork.domain.value_objects import Money, Fee
from ...shared_kernel import OperationType
from ...shared_kernel.achievement_types import AchievementType
from .operation_status import OperationStatus

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
        assert self.status != OperationStatus.CANCELLED, "You cant mark as in progress the operation if the status is cancelled"

        self.in_progress_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = OperationStatus.IN_PROGRESS

    def paid(self) -> None:
        assert self.status != OperationStatus.CANCELLED, "You cant mark as paid the operation if the status is cancelled"
        
        self.updated_at = datetime.now()
        self.completed_at = datetime.now()
        self.status = OperationStatus.PAID
    
    def under_review(self) -> None:
        assert self.status != OperationStatus.UNDER_REVIEW, "Status is already under review"
        
        self.updated_at = datetime.now()
        self.status = OperationStatus.UNDER_REVIEW

    def cancel(self) -> None:
        assert self.status != OperationStatus.CANCELLED, "The operation status is already cancelled"
        
        self.updated_at = datetime.now()
        self.status = OperationStatus.CANCELLED

    def set_achievement(self, achievement_type: AchievementType) -> None:
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
    def revenue(self) -> Money:
        return self.management.amount

    @property
    def fee(self) -> Fee:
        return self.management.fee

    @property
    def broker_fee(self) -> Fee:
        fractions = [self.close, self.capture]
        impactables = [op for op in fractions if op and op.must_impact]
        if any(impactables):
            fee = sum([fraction.fee for fraction in impactables if fraction])# type: ignore
            return self.calculate_management_fee_substracting_partner_tier(tier_partner=fee)
        else:
            return self.management.fee

    @property
    def broker_revenue(self) -> Money:
        from functools import reduce

        fractions = [self.close, self.capture]
        impactables = [op for op in fractions if op and op.must_impact]
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
        assert self.capture and self.capture.must_impact, "Valid capture is setted and " \
        "can't be overwritten" 
            
        self.capture = operation

    def set_close(self, operation: Operation):
        assert self.close and self.close.must_impact, "Valid close is setted and " \
        "can't be overwritten" 

        self.close = operation