from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from src.seedwork.domain.entities import AggregateRoot
from src.seedwork.domain.value_objects import GenericUUID, DateRange, Fee, Money, RenewAlert
from .strategy_status import StrategyStatus
from ...shared_kernel.operation_types import OperationType
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from .decorators import check_status_is_not_discontinued
from .rules import (
    PeriodMustBeOnGoing,
    DaysBeforeRenewAlertMustGreatherThanZero,
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
    StrategyWasCompleted
)

@dataclass
class Strategy(AggregateRoot):
    type: OperationType
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

    def __post_init__(self):
        if not self.deposit:
            self.deposit = Money(amount=0, currency=self.price.currency)
        self.check_rule(DaysBeforeRenewAlertMustGreatherThanZero(days=self.renew_alert.notice_days_threshold))        

    @property
    def completed(self) -> bool:
        return self.accepted_by_customer_id is not None and self.status == StrategyStatus.COMPLETED

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
        return OperationType.get_default_types()
    
    @property
    def default_strategy_status(self) -> List[str]:
        return StrategyStatus.get_default_strategy_status()

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
        self.register_event(StrategyRenewAlertActivated(strategy_id=self.id))
    
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
                strategy_id=self.id,
                period=self.period,
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
                strategy_id=self.id,
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
                strategy_id=self.id,
                type=self.type
            )
        )

    def pause(self) -> None:
        assert self.status != StrategyStatus.PAUSED, "Strategy is already paused"
        assert self.period.on_going, "Period isn't on going"

        self.status = StrategyStatus.PAUSED
        self.register_event(
            StrategyWasPaused(
                strategy_id=self.id,
                type=self.type
            )
        )

    def mark_as_completed(self) -> None:
        self.status = StrategyStatus.COMPLETED
        self.accepted_by_customer_id = GenericUUID.next_id()
        self.register_event(
            StrategyWasCompleted(
                strategy_id=self.id,
                property_id=self.property_id,
                price=self.price,
                period=self.period,
                deposit=self.deposit, #type: ignore
                terms_conditions=self.terms_conditions,
                type=self.type
            )
        )

    @check_status_is_not_discontinued
    def evaluate_expiration(self) -> None:
        if self.period.finished:
            self.status = StrategyStatus.EXPIRED
            self.register_event(StrategyHasExpired(strategy_id=self.id, type=self.type))

    @check_status_is_not_discontinued
    def register_term(self, term: Term) -> None:
        self.terms_conditions.register_term(term)
        self.register_event(TermWasAdded(strategy_id=self.id, term=term))

    def delete_term(self, term_type: TermIdentifier) -> None:
        self.terms_conditions.delete_term(term_type)
        self.register_event(TermWasRemoved(strategy_id=self.id, term_type=term_type))

@dataclass
class Owner:
    name: str
    email: str
    phone: str
    address: str
    city: str
    properties: List[GenericUUID] = field(default_factory=list)