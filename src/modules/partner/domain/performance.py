from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict
from src.seedwork.domain.value_objects import Money, Currency
from src.seedwork.domain.entities import GenericUUID, Entity

@dataclass
class PartnerPerformance:
    period: str
    operations_closed: int = 0
    properties_captured: int = 0
    revenue_generated: Money = field(default_factory=lambda: Money(amount=0))
    last_updated: datetime = field(default_factory=datetime.now)

    def register_close(self, amount: Money) -> None:
        self.operations_closed += 1
        self.revenue_generated += amount
        self.last_updated = datetime.now()

    def register_capture(self, amount: Money) -> None:
        self.properties_captured += 1
        self.revenue_generated += amount
        self.last_updated = datetime.now()

    def add_revenue_generated(self, amount: Money) -> None:
        self.revenue_generated += amount

    def substract_revenue_generated(self, amount: Money) -> None:
        self.revenue_generated += amount

    def as_dict(self) -> Dict:
        return {
            "period": self.period,
            "operations_closed": self.operations_closed,
            "properties_captured": self.properties_captured,
            "revenue_generated": {
                "amount": self.revenue_generated.amount,
                "currency": self.revenue_generated.currency,
            },
            "last_updated": self.last_updated
        }

    @classmethod
    def from_dict(cls, perfomance_data: Dict[str, str]) -> PartnerPerformance:
        return cls(
            period=perfomance_data["period"],
            operations_closed=int(perfomance_data["operations_closed"]),
            properties_captured=int(perfomance_data["properties_captured"]),
            revenue_generated=Money(
                amount=float(perfomance_data["revenue_generated"]["amount"]), #type: ignore
                currency=Currency(perfomance_data["revenue_generated"]["currency"]) #type: ignore
            ),
            last_updated=datetime.fromisoformat((perfomance_data["last_updated"])) #type: ignore
        )