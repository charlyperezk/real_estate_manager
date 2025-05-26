from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from src.seedwork.domain.entities import AggregateRoot
from src.seedwork.domain.value_objects import GenericUUID, DateRange, Fee, Money, RenewAlert
from .strategy_status import StrategyStatus
from .strategy_types import StrategyType
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from .partners import Partners
from .partner import Partner, AchievementType
from .decorators import check_status_is_not_discontinued
from .rules import (
    PeriodMustBeOnGoing,
    DaysBeforeRenewAlertMustGreatherThanZero,
    CaptureAchievementCanBeAddedIfThereIsNoExclusivity
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
    StrategyWasCompleted
)

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
    renew_alert: RenewAlert = field(default=RenewAlert(notice_days_threshold=15))
    status: StrategyStatus = field(default=StrategyStatus.PLANNED)
    accepted_by_customer_id: Optional[GenericUUID] = field(default=None)
    partners: Partners = field(default_factory=Partners)

    def __post_init__(self):
        if not self.deposit:
            self.deposit = Money(amount=0, currency=self.price.currency)
        self.check_rule(DaysBeforeRenewAlertMustGreatherThanZero(days=self.renew_alert.notice_days_threshold))        

    @property
    def completed(self) -> bool:
        return self.accepted_by_customer_id is not None and self.status == StrategyStatus.COMPLETED

    @property
    def shared(self) -> bool:
        return any(self.partners.get_partners())

    @property
    def days_left(self) -> int:
        return self.period.days_left
    
    @property
    def terms_quantity(self) -> int:
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

    def get_partners(self, achievement_type: Optional[AchievementType]=None) -> List[Partner]:
        return self.partners.get_partners(achievement_type=achievement_type)

    def add_partner(self, partner: Partner) -> None:
        self.check_rule(
            CaptureAchievementCanBeAddedIfThereIsNoExclusivity(
                exclusivity=self.exclusivity,
                achievement_type=partner.type
            )
        )
        self.partners.add_partner(partner)
        self.register_event(
            PartnerWasAdded(
                id=partner.id,
                property_id=self.property_id,
                strategy_type=self.type,
                achievement_type=partner.type,
                status=self.status
            )
        )

    def update_partner(self, partner: Partner) -> None:
        self.partners.update_partner(partner)
        self.register_event(
            PartnerWasUpdated(
                id=partner.id,
                property_id=self.property_id,
                strategy_type=self.type,
                achievement_type=partner.type,
                status=self.status
            )
        )

    def delete_partner(self, partner: Partner) -> None:
        self.partners.add_partner(partner)
        self.register_event(
            PartnerWasRemoved(
                id=partner.id,
                property_id=self.property_id,
                strategy_type=self.type,
                achievement_type=partner.type,
                status=self.status
            )
        )

    def within_renew_alert_threshold(self) -> bool:
        return self.period.on_going and self.renew_alert.within_threshold(self.period.days_left)

    @check_status_is_not_discontinued
    def activate_renew_alert(self) -> None:
        assert self.within_renew_alert_threshold(), "Strategy isn't in alert renew period"
        assert not self.renew_alert.active, "Renew alert is already activated"

        self.renew_alert = RenewAlert(
            active=True,
            notice_days_threshold=self.renew_alert.notice_days_threshold
        )
        self.register_event(StrategyRenewAlertActivated(property_id=self.property_id))
    
    @check_status_is_not_discontinued
    def extend_period(self, **period) -> None:        
        self.period = self.period.extended(**period)
        
        if self.renew_alert.active:
            self.renew_alert = RenewAlert(
                active=False,
                notice_days_threshold=self.renew_alert.notice_days_threshold
            )

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

    def mark_as_completed(self) -> None:
        self.status = StrategyStatus.COMPLETED
        self.accepted_by_customer_id = GenericUUID.next_id()
        self.register_event(
            StrategyWasCompleted(
                property_id=self.property_id,
                price=self.price,
                period=self.period,
                deposit=self.deposit, #type: ignore
                terms_conditions=self.terms_conditions,
                type=self.type,
                partners=self.partners
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