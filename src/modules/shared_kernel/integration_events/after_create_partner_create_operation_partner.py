from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.application.events import IntegrationEvent
from .. import PartnershipStatus, Partnership, PartnershipType

class OnAfterCreatePartnerCreateOperationPartner(IntegrationEvent):
    partner_id: GenericUUID
    user_id: GenericUUID
    status: PartnershipStatus
    partnership: Partnership
    type: PartnershipType
    name: str