from typing import List
from src.seedwork.domain.value_objects import DateRange
from src.seedwork.domain.rules import BusinessRule
from .terms_and_conditions import Term, TermIdentifier
from .entities import StrategyStatus
from .partner import Partner, AchievementType

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
        
class AchievementMustBeUnique(BusinessRule):
    achievement_type: str
    partners: List[Partner]

    _message = "Partner type already exists"

    def is_broken(self) -> bool:
        return any((partner.type == self.achievement_type for partner in self.partners))

class CaptureAchievementCanBeAddedIfThereIsNoExclusivity(BusinessRule):
    exclusivity: bool
    achievement_type: str

    _message = "Can't add associate partner if there is exclusivity"

    def is_broken(self) -> bool:
        return self.exclusivity and self.achievement_type == AchievementType.CAPTURE

# TermsAndConditions rules:
class TermTypeMustNotAlreadyBeInTerms(BusinessRule):
    identifier: TermIdentifier
    terms: List[Term]

    _message = "A term with the same identifier already exists in Terms and Conditions"

    def is_broken(self) -> bool:
        return any((term.type == self.identifier for term in self.terms))