from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from src.seedwork.domain.entities import AggregateRoot
from src.seedwork.domain.value_objects import GenericUUID, DateRange, Fee, Money, RenewAlert
from .strategy_status import StrategyStatus
from ...shared_kernel.operation_types import OperationType
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from .rules import (
    PeriodMustBeOnGoing,
    DaysBeforeRenewAlertMustGreatherThanZero,
    StrategyMustNotBeAlreadyActivated,
    StrategyMustNotBeCompleted,
    StrategyMustNotBeAlreadyPaused,
    StrategyMustNotBeDiscontinued,
    RenewAlertMustNotBeActive,
    RenewAlertMustHaveExceededTheThreshold
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

    def __post_init__(self):
        self.check_rule(DaysBeforeRenewAlertMustGreatherThanZero(days=self.renew_alert.notice_days_threshold))        

        if not self.deposit:
            self.deposit = Money(amount=0, currency=self.price.currency)

    @property
    def completed(self) -> bool:
        return self.status == StrategyStatus.COMPLETED

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
        self.check_rule(PeriodMustBeOnGoing(period=self.period))
        return self.renew_alert.within_threshold(self.period.days_left)

    def activate_renew_alert(self) -> None:
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))
        self.check_rule(RenewAlertMustNotBeActive(active=self.renew_alert.active))
        self.check_rule(
            RenewAlertMustHaveExceededTheThreshold(
                renew_alert=self.renew_alert,
                days_left=self.period.days_left
            )
        )

        self.renew_alert = RenewAlert(
            active=True,
            notice_days_threshold=self.renew_alert.notice_days_threshold
        )
        self.register_event(StrategyRenewAlertActivated(strategy_id=self.id))
    
    def extend_period(self, **period) -> None:        
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))        

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
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))
        self.check_rule(StrategyMustNotBeAlreadyActivated(status=self.status))
        self.check_rule(StrategyMustNotBeCompleted(status=self.status))
        self.check_rule(PeriodMustBeOnGoing(period=self.period))
        
        self.status = StrategyStatus.ACTIVE
        self.register_event(
            StrategyWasActivated(
                property_id=self.property_id,
                strategy_id=self.id,
                price=self.price,
                fee=self.fee,
                period=self.period,
                deposit=self.deposit, #type: ignore
                terms_conditions=self.terms_conditions,
                type=self.type
            )
        )

    def discontinue(self) -> None:
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))

        self.status = StrategyStatus.DISCONTINUED
        self.period = self.period.stopped()
        self.register_event(
            StrategyWasDiscontinued(
                strategy_id=self.id,
                type=self.type
            )
        )

    def pause(self) -> None:
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))
        self.check_rule(StrategyMustNotBeAlreadyPaused(status=self.status))
        self.check_rule(StrategyMustNotBeCompleted(status=self.status))
        self.check_rule(PeriodMustBeOnGoing(period=self.period))

        self.status = StrategyStatus.PAUSED
        self.register_event(
            StrategyWasPaused(
                strategy_id=self.id,
                type=self.type
            )
        )

    def mark_as_completed(self) -> None:
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))
        self.check_rule(StrategyMustNotBeCompleted(status=self.status))
        
        self.status = StrategyStatus.COMPLETED
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

    def evaluate_expiration(self) -> None:
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))

        if self.period.finished:
            self.status = StrategyStatus.EXPIRED
            self.register_event(StrategyHasExpired(strategy_id=self.id, type=self.type))

    def register_term(self, term: Term) -> None:
        self.check_rule(StrategyMustNotBeDiscontinued(status=self.status))
        self.check_rule(StrategyMustNotBeCompleted(status=self.status))
        
        self.terms_conditions.register_term(term)
        self.register_event(TermWasAdded(strategy_id=self.id, term=term))

    def delete_term(self, term_type: TermIdentifier) -> None:
        self.check_rule(StrategyMustNotBeCompleted(status=self.status))
        
        self.terms_conditions.delete_term(term_type)
        self.register_event(TermWasRemoved(strategy_id=self.id, term_type=term_type))