from src.seedwork.domain.value_objects import GenericUUID, Money, DateRange, Fee
from src.seedwork.domain.events import DomainEvent
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from ...shared_kernel.operation_types import OperationType
from .strategy_status import StrategyStatus

"""
I'm following the pgorecki approach with events management. But you can see this article to find more approaches:
https://medium.com/@dkraczkowski/events-in-domain-driven-design-event-propagation-strategies-b30d8df046e2
"""

# Strategy events
class StrategyWasCreated(DomainEvent):
    strategy_id: GenericUUID
    property_id: GenericUUID
    price: Money
    fee: Fee
    deposit: Money
    terms_conditions: TermsAndConditions
    type: OperationType
    period: DateRange

class StrategyWasActivated(StrategyWasCreated):
    ...

class StrategyWasDiscontinued(DomainEvent):
    strategy_id: GenericUUID
    type: OperationType

class StrategyWasPaused(StrategyWasDiscontinued):
    ...

class StrategyHasExpired(StrategyWasDiscontinued):
    ...

class StrategyWasCompleted(StrategyWasActivated):
    ...

class PeriodWasExtended(DomainEvent):
    strategy_id: GenericUUID
    period: DateRange
    status: StrategyStatus

class StrategyRenewAlertActivated(DomainEvent):
    strategy_id: GenericUUID

class PeriodHasExpired(StrategyRenewAlertActivated):
    ...

class PeriodWasStopped(PeriodHasExpired):
    ...

class TermWasAdded(DomainEvent):
    strategy_id: GenericUUID
    term: Term

class TermWasRemoved(DomainEvent):
    strategy_id: GenericUUID
    term_type: TermIdentifier