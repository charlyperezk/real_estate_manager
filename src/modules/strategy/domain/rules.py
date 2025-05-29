from typing import List
from src.seedwork.domain.value_objects import DateRange, RenewAlert
from src.seedwork.domain.rules import BusinessRule
from .terms_and_conditions import Term, TermIdentifier
from .entities import StrategyStatus

# Strategy rules:
class PeriodMustBeOnGoing(BusinessRule):
    period: DateRange
    
    _message = "Period must be on going"

    def is_broken(self) -> bool:
        return not self.period.on_going

class PeriodMustBeValidToSetActivateStatus(BusinessRule):
    period: DateRange
    status: StrategyStatus
    
    _message = "Can't activate an strategy if the period doesn't start"

    def is_broken(self) -> bool:
        return not self.period.already_started and self.status == StrategyStatus.ACTIVE

class PeriodMustBePlannedToSetPlannedStatus(BusinessRule):
    period: DateRange
    status: StrategyStatus
    
    _message = "Can't activate an strategy if the period doesn't start"

    def is_broken(self) -> bool:
        return self.period.already_started and self.status == StrategyStatus.PLANNED

class DaysBeforeRenewAlertMustGreatherThanZero(BusinessRule):
    days: int

    _message = "Days before renew alert must be positive"

    def is_broken(self) -> bool:
        return self.days < 0
        
class TermTypeMustNotAlreadyBeInTerms(BusinessRule):
    identifier: TermIdentifier
    terms: List[Term]

    _message = "A term with the same identifier already exists in Terms and Conditions"

    def is_broken(self) -> bool:
        return any((term.type == self.identifier for term in self.terms))
    
class StrategyMustNotBeCompleted(BusinessRule):
    status: StrategyStatus

    _message = "Strategy is already completed"

    def is_broken(self) -> bool:
        return self.status == StrategyStatus.COMPLETED

class StrategyMustNotBeAlreadyActivated(BusinessRule):
    status: StrategyStatus

    _message = "Strategy is already activated"

    def is_broken(self) -> bool:
        return self.status == StrategyStatus.ACTIVE

class StrategyMustNotBeAlreadyPaused(BusinessRule):
    status: StrategyStatus

    _message = "Strategy is already paused"

    def is_broken(self) -> bool:
        return self.status == StrategyStatus.PAUSED

class StrategyMustNotBeDiscontinued(BusinessRule):
    status: StrategyStatus

    _message = "Strategy is discontinued"

    def is_broken(self) -> bool:
        return self.status == StrategyStatus.DISCONTINUED
    
class RenewAlertMustNotBeActive(BusinessRule):
    active: bool

    _message = "Renew alert is already activated"

    def is_broken(self) -> bool:
        return self.active
    
class RenewAlertMustHaveExceededTheThreshold(BusinessRule):
    renew_alert: RenewAlert
    days_left: int

    _message = "Period must have exceeded the threshold"

    def is_broken(self) -> bool:
        return not self.renew_alert.within_threshold(self.days_left)