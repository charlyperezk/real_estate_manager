from __future__ import annotations
from typing import Dict
from dataclasses import dataclass, field
from .performance import PartnerPerformance
from .utils import current_period
from src.seedwork.domain.value_objects import GenericUUID, Money

@dataclass
class TargetsLog:
    targets: Dict[str, PartnerPerformance] = field(default_factory=dict)

    def __post_init__(self):
        self.get_or_create_period_performance(period=current_period())

    def get_or_create_period_performance(self, period: str) -> PartnerPerformance:
        #TODO: Period must be current period or less
        performance = self.targets.get(period, None)
        
        if not performance:
            performance = PartnerPerformance(period=period)
            self.targets[period] = performance
            return performance
        
        return performance
        
    def get_all(self) -> Dict[str, PartnerPerformance]:
        return self.targets

    def register_close(self, period: str, amount: Money) -> None:
        performance = self.get_or_create_period_performance(period=period)
        performance.register_close(amount=amount)

    def register_capture(self, period: str, amount: Money) -> None:
        performance = self.get_or_create_period_performance(period=period)
        performance.register_capture(amount=amount)

    def persist(self, period: str, performance: PartnerPerformance) -> None:
        self.targets[period] = performance

    def remove(self, period: str) -> None:
        del self.targets[period]

    def as_dict(self) -> Dict:
        return {
            period: performance.as_dict()
            for period, performance in self.targets.items()
        }

    @classmethod
    def from_dict(cls, targets_data: Dict) -> TargetsLog:
        return cls(
            targets={
                period: PartnerPerformance.from_dict(performance)
                for period, performance in targets_data.items()
            }
        )
