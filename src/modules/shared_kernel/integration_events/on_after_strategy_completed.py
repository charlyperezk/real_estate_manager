from src.seedwork.domain.value_objects import GenericUUID, Money, Fee
from src.seedwork.application.events import IntegrationEvent

class OnAfterStrategyCompleted(IntegrationEvent):
    strategy_id: GenericUUID
    price: Money
    fee: Fee