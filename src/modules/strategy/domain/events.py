from src.seedwork.domain.value_objects import GenericUUID, Money, DateRange
from src.seedwork.domain.events import DomainEvent
from .terms_and_conditions import TermsAndConditions, Term, TermIdentifier
from .strategy_types import StrategyType
from .strategy_status import StrategyStatus
from .partners import AchievementType, Partners

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

class StrategyWasCompleted(StrategyWasActivated):
    partners: Partners

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
    strategy_type: StrategyType
    achievement_type: AchievementType
    status: StrategyStatus

class PartnerWasRemoved(PartnerWasAdded):
    ...

class PartnerWasUpdated(PartnerWasAdded):
    ...