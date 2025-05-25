from dataclasses import dataclass, field
from typing import List, Optional
from src.seedwork.domain.mixins import check_rule
from .value_objects import Fee
from .rules import PartnerMustBeUnique, PartnerCanBeAddedIfFeeIsLessThan75
from .value_objects.partner import Partner, PartnerType

@dataclass
class Partners:
    partners: List[Partner] = field(default_factory=list)

    @staticmethod
    def get_default_term_types() -> List[str]:
        return [value.value for value in list(PartnerType)]

    def get_partners(self, type: Optional[PartnerType]=None):
        partners = self.partners
        if type:
            partners = list(filter(lambda partner: partner.type == type, partners))
        return partners

    def calculate_sum_of_participation(self) -> Fee:
        partners_fee_sum = sum((partner.fee.value for partner in self.partners))
        if partners_fee_sum:
            return Fee(value=partners_fee_sum)
        else:
            return Fee(value=0)

    def add_partner(self, partner: Partner):
        check_rule(PartnerMustBeUnique(partner_type=partner.type, partners=self.partners))        
        check_rule(
            PartnerCanBeAddedIfFeeIsLessThan75(
                fee=partner.fee.value,
                partners_fee_sum=self.calculate_sum_of_participation().value
            )
        )
        self.add_partner(partner)

    def delete_partner(self, partner_type: PartnerType):
        partner = self.get_partners(type=partner_type)
        assert partner, "Partner not found"
        self.partners = list(filter(lambda partner: partner.type != partner_type, self.partners))

    def update_partner(self, partner: Partner):
        self.delete_partner(partner.type)
        check_rule(
            PartnerCanBeAddedIfFeeIsLessThan75(
                fee=partner.fee.value,
                partners_fee_sum=self.calculate_sum_of_participation().value
            )
        )
        self.add_partner(partner)