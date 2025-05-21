from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List

from .value_objects.date_range import DateRange
from .value_objects.fee import Fee
from .value_objects.money import Money
from .strategy_status import StrategyStatus
from .strategy_types import StrategyType
from .terms_and_conditions import TermsAndConditions, Term

@dataclass
class Strategy:
    type: StrategyType
    price: Money
    accepted: bool
    fee: Fee
    period: DateRange
    status: StrategyStatus
    shared: bool
    exclusivity: bool
    terms_conditions: TermsAndConditions

    @property
    def days_left(self) -> int:
        return self.period.days_left
    
    @property
    def terms_quantity(self) -> int:
        return self.terms_conditions.registered_terms
    
    @property
    def term_types(self) -> List[str]:
        return Term.get_default_term_types()