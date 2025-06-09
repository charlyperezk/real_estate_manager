from datetime import datetime
from src.seedwork.domain.value_objects import GenericUUID, Money, Period, Fee
from src.seedwork.domain.events import DomainEvent
from ...shared_kernel.achievement_types import AchievementType
from ...shared_kernel.operation_types import OperationType
from .operation_status import OperationStatus

class RealEstateOperationWasInitialized(DomainEvent):
    operation_id: GenericUUID
    property_id: GenericUUID
    type: OperationType
    status: OperationStatus
    created_at: datetime
    description: str
    revenue: Money

class PartnerAchievementOperationRegistered(DomainEvent):
    operation_id: GenericUUID
    property_id: GenericUUID
    partner_id: GenericUUID
    type: OperationType
    achievement_type: AchievementType
    status: OperationStatus
    created_at: datetime
    description: str
    revenue: Money
    period: Period

class OperationStatusChangedToInProgress(DomainEvent):
    partner_id: GenericUUID
    revenue: Money
    fee: Fee
    achievement_type: AchievementType
    period: Period