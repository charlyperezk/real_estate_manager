from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.application.events import IntegrationEvent

class OnAfterPartnerBanned(IntegrationEvent):
    partner_id: GenericUUID
    review_operations: bool