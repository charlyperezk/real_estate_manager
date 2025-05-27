from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.domain.events import DomainEvent
from .types import PartnershipType
from .operations import Operations, Operation
from .value_objects.partner_fee import PartnerFee

class PartnershipWasActivated(DomainEvent):
    partner_id: GenericUUID
    user_id: GenericUUID
    type: PartnershipType
    operations: Operations

class PartnershipWasFinished(PartnershipWasActivated):
    ...

class PartnerFeeAddedToPartnership(DomainEvent):
    partner_id: GenericUUID
    fee: PartnerFee

class PartnerFeeUpdated(PartnerFeeAddedToPartnership):
    ...

class PartnerStatusWasChanged(PartnerFeeAddedToPartnership):
    ...

class OperationAddedToPartner(DomainEvent):
    partner_id: GenericUUID
    operation: Operation

class OperationDeletedFromPartner(OperationAddedToPartner):
    ...

class PartnerOperationStatusChangedToPaid(OperationAddedToPartner):
    ...

class PartnerOperationStatusChangedToInProgress(OperationAddedToPartner):
    ...

class PartnerOperationStatusChangedToCancelled(OperationAddedToPartner):
    ...