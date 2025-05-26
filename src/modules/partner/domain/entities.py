from datetime import datetime
from typing import List
from dataclasses import dataclass, field
from src.seedwork.domain.entities import GenericUUID, AggregateRoot
from .partnership import Partnership, OperationType
from .status import PartnershipStatus
from .types import PartnershipType
from .value_objects.partner_fee import PartnerFee

@dataclass
class Partner(AggregateRoot):
    name: str
    user_id: GenericUUID
    type: PartnershipType
    partnership: Partnership
    status: PartnershipStatus = field(default=PartnershipStatus.ACTIVE)
    created_at: datetime = field(default_factory=datetime.now)

    def add_fee(self, partner_fee: PartnerFee) -> None:
        self.partnership.add_fee(partner_fee)

    def update_fee(self, partner_fee: PartnerFee) -> None:
        self.partnership.update_fee(partner_fee)

    def delete_fee(self, operation_type: OperationType) -> None:
        self.partnership.delete_fee(operation_type)

    def get_fees(self, operation_type: OperationType) -> List[PartnerFee]:
        return self.partnership.get_fees(type=operation_type)
    
    def set_status(self, status: PartnershipStatus) -> None:
        self.status = status