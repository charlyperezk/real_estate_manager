from typing import List, Optional, List
from dataclasses import dataclass, field
from .operation_types import OperationType
from .value_objects.partner_fee import PartnerFee

@dataclass
class Partnership:
    fees: List[PartnerFee] = field(default_factory=list)        

    def get_fees(self, type: Optional[OperationType]=None) -> List[PartnerFee]:
        fees = self.fees
        if type:
            fees = [fee for fee in fees if fee.operation_type == type]
        return fees
    
    def any_rent_fee_is_declared(self) -> bool:
        return any(self.get_fees(type=OperationType.RENT))
    
    def any_sell_fee_is_declared(self) -> bool:
        return any(self.get_fees(type=OperationType.SELL))
    
    def add_fee(self, partner_fee: PartnerFee) -> None:
        assert not self.get_fees(partner_fee.operation_type), f"{partner_fee.operation_type} is already setted. You must update it."
        self.fees.append(partner_fee)

    def update_fee(self, partner_fee: PartnerFee) -> None:
        assert self.get_fees(partner_fee.operation_type), f"{partner_fee.operation_type} Fee not found."
        self.delete_fee(partner_fee.operation_type)
        self.add_fee(partner_fee)

    def delete_fee(self, operation_type: OperationType) -> None:
        assert self.get_fees(operation_type), f"{operation_type} Fee not found."
        self.fees = [fee for fee in self.fees if fee.operation_type != operation_type]