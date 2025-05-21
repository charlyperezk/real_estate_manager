from typing import List
from src.seedwork.domain.rules import BusinessRule
from .terms_and_conditions import Term, TermIdentifier
from .value_objects.date_range import DateRange
from .strategy_status import StrategyStatus

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

class DaysBeforeRenewAlertMustBePositive(BusinessRule):
    days: int

    _message = "Days before renew alert must be positive"

    def is_broken(self) -> bool:
        return self.days < 0
    
# TermsAndConditions rules:
class TermTypeMustNotAlreadyBeInTerms(BusinessRule):
    identifier: TermIdentifier
    terms: List[Term]

    _message = "A term with the same identifier already exists in Terms and Conditions"

    def is_broken(self) -> bool:
        return any((term.type == self.identifier for term in self.terms))