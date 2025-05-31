from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.application.events import IntegrationEvent
from .. import PartnershipStatus

class OnAfterActivatePartner(IntegrationEvent):
    partner_id: GenericUUID
    user_id: GenericUUID
    status: PartnershipStatus
    name: str