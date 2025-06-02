from __future__ import annotations
from typing import Dict
from dataclasses import dataclass, field
from .performance import PartnerPerformance
from src.seedwork.domain.value_objects import Money
from ...shared_kernel import Period

@dataclass
class TargetsLog:
    targets: Dict[str, PartnerPerformance] = field(default_factory=dict)

    def __post_init__(self):
        self.get_or_create_period_performance(period=Period.get_current_period())

    def get_or_create_period_performance(self, period: Period) -> PartnerPerformance:
        performance = self.targets.get(period.representation(), None)
        if not performance:
            performance = PartnerPerformance(period=period)
            self.targets[period.representation()] = performance
            return performance
        
        return performance
        
    def get_all(self) -> Dict[str, PartnerPerformance]:
        return self.targets

    def register_close(self, period: Period, amount: Money) -> None:
        performance = self.get_or_create_period_performance(period=period)
        performance.register_close(amount=amount)

    def register_capture(self, period: Period, amount: Money) -> None:
        performance = self.get_or_create_period_performance(period=period)
        performance.register_capture(amount=amount)

    def persist(self, period: Period, performance: PartnerPerformance) -> None:
        self.targets[period.representation()] = performance

    def remove(self, period: Period) -> None:
        del self.targets[period.representation()]

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
