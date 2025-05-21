from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from ..seedwork.domain.entities import AggregateRoot
from ..seedwork.domain.value_objects import GenericUUID
from .value_objects.date_range import DateRange
from .value_objects.fee import Fee
from .value_objects.money import Money
from .strategy_status import StrategyStatus
from .strategy_types import StrategyType
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from .decorators import check_status_is_not_discontinued
from .rules import (
    PeriodMustBeOnGoing,
    DaysBeforeRenewAlertMustBePositive
)
from .events import (
    StrategyWasActivated,
    StrategyWasDiscontinued,
    PeriodWasExtended,
    PeriodHasExpired,
    PeriodWasStopped
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
    renew_alert: bool = field(default=False)
    days_before_renew_alert: int = field(default=15)
    status: StrategyStatus = field(default=StrategyStatus.ACTIVE)
    accepted: bool = field(default=False)

    def __post_init__(self):
        if not self.deposit:
            self.deposit = Money(amount=0, currency=self.price.currency)
        self.check_rule(DaysBeforeRenewAlertMustBePositive(days=self.days_before_renew_alert))        

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

    def discontinue(self) -> None:
        assert self.status != StrategyStatus.DISCONTINUED, "Strategy is already discontinued"
        
        self.status = StrategyStatus.DISCONTINUED
        self.period = self.period.stopped()
        self.register_event(
            StrategyWasDiscontinued(
                property_id=self.property_id,
                type=self.type
            )
        )

    @check_status_is_not_discontinued
    def extend_period(self, **period):        
        self.period = self.period.extended(**period)
        self.register_event(
            PeriodWasExtended(
                period=self.period,
                property_id=self.property_id,
                status=self.status
            )
        )

    @check_status_is_not_discontinued
    def register_term(self, term: Term) -> None:
        self.terms_conditions.register_term(term)    

    def unregister_term(self, term_type: TermIdentifier) -> None:
        self.terms_conditions.unregister_term(term_type)