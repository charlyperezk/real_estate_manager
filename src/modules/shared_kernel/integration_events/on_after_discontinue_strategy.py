from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.application.events import IntegrationEvent

class OnAfterDiscontinueStrategy(IntegrationEvent):
    strategy_id: GenericUUID