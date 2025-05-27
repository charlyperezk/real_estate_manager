from typing import Union
from datetime import datetime
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.domain.events import DomainEvent
from ...shared_kernel.achievement_types import AchievementType
from ...shared_kernel.operation_types import OperationType
from ...shared_kernel.status import OperationStatus

class ManagementOperationWasStarted(DomainEvent):
    operation_id: GenericUUID
    property_id: GenericUUID
    type: OperationType
    status: OperationStatus
    created_at: datetime
    description: str

class PartnerOperationWasCreated(DomainEvent):
    operation_id: GenericUUID
    property_id: GenericUUID
    partner_id: Union[str, GenericUUID]
    type: OperationType
    user_id: GenericUUID
    achievement_type: AchievementType
    status: OperationStatus
    created_at: datetime
    description: str