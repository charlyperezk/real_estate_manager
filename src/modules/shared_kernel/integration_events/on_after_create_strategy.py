from src.seedwork.domain.value_objects import GenericUUID, Money, Fee
from src.seedwork.application.events import IntegrationEvent
from .. import OperationType

class OnAfterCreateStrategy(IntegrationEvent):
    property_id: GenericUUID
    strategy_id: GenericUUID
    price: Money
    fee: Fee
    type: OperationType