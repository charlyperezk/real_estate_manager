from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.application.events import IntegrationEvent

class OnAfterFinishPartnerFinishOperationPartner(IntegrationEvent):
    partner_id: GenericUUID