from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from src.seedwork.domain.entities import Entity, AggregateRoot
from src.seedwork.domain.value_objects import GenericUUID
from .value_objects.date_range import DateRange
from .value_objects.fee import Fee
from .value_objects.money import Money
from .strategy_status import StrategyStatus
from .strategy_types import StrategyType
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from .partners import Partners
from .partner import Partner, PartnerType, Participation
from .decorators import check_status_is_not_discontinued
from .rules import (
    PeriodMustBeOnGoing,
    DaysBeforeRenewAlertMustBePositive,
    AssociatePartnerCanBeAddedIfThereIsNoExclusivity
)
from .events import (
    StrategyWasActivated,
    StrategyWasPaused,
    StrategyWasDiscontinued,
    StrategyRenewAlertActivated,
    PeriodWasExtended,
    StrategyHasExpired,
    TermWasAdded,
    TermWasRemoved,
    PartnerWasAdded,
    PartnerWasRemoved,
    PartnerWasUpdated,
)

# @dataclass
# class Confirmation(Entity):
#     customer_id: GenericUUID
#     timestamp: datetime

@dataclass
class Strategy(AggregateRoot):
    type: StrategyType
    price: Money
    fee: Fee
    exclusivity: bool
    property_id: GenericUUID
    deposit: Optional[Money] = field(default=None)
    terms_conditions: TermsAndConditions = field(default_factory=TermsAndConditions)
    period: DateRange = field(default=DateRange.from_now_to(weeks=12))
    renew_alert: bool = field(default=False)
    days_before_renew_alert: int = field(default=15)
    status: StrategyStatus = field(default=StrategyStatus.ACTIVE)
    accepted_by_customer_id: Optional[GenericUUID] = field(default=None)
    partners: Partners = field(default_factory=Partners)

    def __post_init__(self):
        if not self.deposit:
            self.deposit = Money(amount=0, currency=self.price.currency)
        self.check_rule(DaysBeforeRenewAlertMustBePositive(days=self.days_before_renew_alert))        

    @property
    def accepted(self) -> bool:
        """
        Returns if the strategy was accepted by a customer
        """
        return self.accepted_by_customer_id is not None

    @property
    def shared(self) -> bool:
        """
        Returns if the strategy has a comercialization partnership
        """
        return any(self.partners.get_partners())

    @property
    def days_left(self) -> int:
        """
        Days until the end of the period
        """
        return self.period.days_left
    
    @property
    def terms_quantity(self) -> int:
        """
        Number of registered terms and conditions
        """
        return self.terms_conditions.registered_terms
    
    @property
    def term_default_types(self) -> List[str]:
        return Term.get_default_term_types()
    
    @property
    def available_strategy_types(self) -> List[str]:
        return StrategyType.get_default_strategy_types()
    
    @property
    def default_strategy_status(self) -> List[str]:
        return StrategyStatus.get_default_strategy_status()

    def get_partners(self, type: Optional[PartnerType]=None) -> List[Partner]:
        return self.partners.get_partners(type=type)

    def partner_has_participation(self, partner_id: GenericUUID) -> bool:
        return any([partner for partner in self.get_partners() if partner.id == partner_id])

    def get_participation_by_partner_id(self, partner_id: GenericUUID) -> Participation:
        assert self.partner_has_participation(partner_id), "Partner doesn't have any participation"
        return next((partner.participation for partner in self.get_partners() if partner.id == partner_id))

    def add_partner(self, partner: Partner) -> None:
        self.check_rule(
            AssociatePartnerCanBeAddedIfThereIsNoExclusivity(
                exclusivity=self.exclusivity,
                partner_type=partner.type
            )
        )
        self.partners.add_partner(partner)
        self.register_event(
            PartnerWasAdded(
                id=partner.id,
                property_id=self.property_id,
                partner_type=partner.type,
                fee=partner.fee.value,
                exclusivity=self.exclusivity,
                status=self.status
            )
        )

    def update_partner(self, partner: Partner) -> None:
        self.partners.update_partner(partner)
        self.register_event(
            PartnerWasUpdated(
                id=partner.id,
                property_id=self.property_id,
                partner_type=partner.type,
                fee=partner.fee.value,
                exclusivity=self.exclusivity,
                status=self.status
            )
        )

    def delete_partner(self, partner: Partner) -> None:
        self.partners.add_partner(partner)
        self.register_event(
            PartnerWasRemoved(
                id=partner.id,
                property_id=self.property_id,
                partner_type=partner.type,
                fee=partner.fee.value,
                exclusivity=self.exclusivity,
                status=self.status
            )
        )

    def calculate_fee(self, exclude_partners: bool=False) -> Money:
        fee = self.fee
        if exclude_partners:
            assert self.shared, "Strategy doesn't have a partner associated"
            partners_fee = self.partners.calculate_sum_of_participation().value
            fee = Fee(value=(self.fee.value * partners_fee) / 100) # type: ignore
        
        return self.price.calculate_fee_amount(fee)

    def calculate_amount_discounting_fee(self) -> Money:
        return self.price.calculate_amount_discounting_fee(self.fee)

    def is_in_renew_alert_period(self) -> bool:
        return self.period.on_going and self.period.days_left < self.days_before_renew_alert

    @check_status_is_not_discontinued
    def activate_renew_alert(self) -> None:
        assert self.is_in_renew_alert_period(), "Strategy isn't in alert renew period"
        assert not self.renew_alert, "Renew alert is already activated"

        self.renew_alert = True
        self.register_event(StrategyRenewAlertActivated(property_id=self.property_id))
    
    @check_status_is_not_discontinued
    def extend_period(self, **period) -> None:        
        self.period = self.period.extended(**period)
        self.register_event(
            PeriodWasExtended(
                period=self.period,
                property_id=self.property_id,
                status=self.status
            )
        )

    def activate(self) -> None:
        assert self.status != StrategyStatus.ACTIVE, "Strategy is already active"
        self.check_rule(PeriodMustBeOnGoing(period=self.period))
        
        self.status = StrategyStatus.ACTIVE
        self.register_event(
            StrategyWasActivated(
                property_id=self.property_id,
                price=self.price,
                period=self.period,
                deposit=self.deposit, #type: ignore
                terms_conditions=self.terms_conditions,
                type=self.type
            )
        )

    @check_status_is_not_discontinued
    def discontinue(self) -> None:        
        self.status = StrategyStatus.DISCONTINUED
        self.period = self.period.stopped()
        self.register_event(
            StrategyWasDiscontinued(
                property_id=self.property_id,
                type=self.type
            )
        )

    def pause(self) -> None:
        assert self.status != StrategyStatus.PAUSED, "Strategy is already paused"
        assert self.period.on_going, "Period isn't on going"

        self.status = StrategyStatus.PAUSED
        self.register_event(
            StrategyWasPaused(
                property_id=self.property_id,
                type=self.type
            )
        )

    @check_status_is_not_discontinued
    def evaluate_expiration(self) -> None:
        if self.period.finished:
            self.status = StrategyStatus.EXPIRED
            self.register_event(StrategyHasExpired(property_id=self.property_id, type=self.type))

    @check_status_is_not_discontinued
    def register_term(self, term: Term) -> None:
        self.terms_conditions.register_term(term)
        self.register_event(TermWasAdded(property_id=self.property_id, term=term))

    def delete_term(self, term_type: TermIdentifier) -> None:
        self.terms_conditions.delete_term(term_type)
        self.register_event(TermWasRemoved(property_id=self.property_id, term_type=term_type))

@dataclass
class Owner:
    name: str
    email: str
    phone: str
    address: str
    city: str
    properties: List[GenericUUID] = field(default_factory=list)