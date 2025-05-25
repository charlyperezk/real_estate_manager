from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.domain.events import DomainEvent
from .value_objects.money import Money
from .value_objects.date_range import DateRange
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from .strategy_types import StrategyType
from .strategy_status import StrategyStatus

"""
I'm following the pgorecki approach with events management. But you can see this article to find more approaches:
https://medium.com/@dkraczkowski/events-in-domain-driven-design-event-propagation-strategies-b30d8df046e2
"""

# Strategy events
class StrategyWasActivated(DomainEvent):
    property_id: GenericUUID
    price: Money
    deposit: Money
    terms_conditions: TermsAndConditions
    type: StrategyType
    period: DateRange

class StrategyWasDiscontinued(DomainEvent):
    property_id: GenericUUID
    type: StrategyType

class StrategyWasPaused(StrategyWasDiscontinued):
    ...

class StrategyHasExpired(StrategyWasDiscontinued):
    ...

class PeriodWasExtended(DomainEvent):
    property_id: GenericUUID
    period: DateRange
    status: StrategyStatus

class StrategyRenewAlertActivated(DomainEvent):
    property_id: GenericUUID

class PeriodHasExpired(StrategyRenewAlertActivated):
    property_id: GenericUUID

class PeriodWasStopped(PeriodHasExpired):
    property_id: GenericUUID

class TermWasAdded(DomainEvent):
    property_id: GenericUUID
    term: Term

class TermWasRemoved(DomainEvent):
    property_id: GenericUUID
    term_type: TermIdentifier

class PartnerWasAdded(DomainEvent):
    property_id: GenericUUID
    partner_type: str
    fee: float
    exclusivity: bool
    status: StrategyStatus

class PartnerWasRemoved(PartnerWasAdded):
    ...

class PartnerWasUpdated(PartnerWasAdded):
    ...