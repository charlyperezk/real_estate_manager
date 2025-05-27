from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Fee, Money
from src.seedwork.infrastructure.logging import Logger
from src.seedwork.application.events import IntegrationEvent
from ...shared_kernel.operation_types import OperationType

class OnAfterCreateStrategyCreateManagementOperation(IntegrationEvent):
    property_id: GenericUUID
    strategy_id: GenericUUID
    type: OperationType
    fee: Fee
    amount: Money
    description: str
