from __future__ import annotations
from dataclasses import dataclass, field, replace

@dataclass(frozen=True)
class RenewAlert:
    active: bool = field(default=False) 
    notice_days_threshold: int = field(default=15) 

    def within_threshold(self, days_left: int) -> bool:
        return days_left > self.notice_days_threshold

    def activated(self) -> RenewAlert:
        return replace(self, active=True)        