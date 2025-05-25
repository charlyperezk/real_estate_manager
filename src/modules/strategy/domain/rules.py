from typing import List
from src.seedwork.domain.rules import BusinessRule
from .terms_and_conditions import Term, TermIdentifier
from .value_objects.date_range import DateRange
from .entities import StrategyStatus
from .value_objects.partner import Partner, PartnerType

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
    
class PartnerCanBeAddedIfFeeIsLessThan75(BusinessRule):
    fee: float
    partners_fee_sum: float

    _message = "Sum of partner fees can't be greather than 75%"

    def is_broken(self) -> bool:
        return (self.fee + self.partners_fee_sum) > 75
    
class PartnerMustBeUnique(BusinessRule):
    partner_type: str
    partners: List[Partner]

    _message = "Partner type already exists"

    def is_broken(self) -> bool:
        return any((partner.type == self.partner_type for partner in self.partners))

class AssociatePartnerCanBeAddedIfThereIsNoExclusivity(BusinessRule):
    exclusivity: bool
    partner_type: str

    _message = "Can't add associate partner if there is exclusivity"

    def is_broken(self) -> bool:
        return self.exclusivity and self.partner_type == PartnerType.ASSOCIATE

# TermsAndConditions rules:
class TermTypeMustNotAlreadyBeInTerms(BusinessRule):
    identifier: TermIdentifier
    terms: List[Term]

    _message = "A term with the same identifier already exists in Terms and Conditions"

    def is_broken(self) -> bool:
        return any((term.type == self.identifier for term in self.terms))