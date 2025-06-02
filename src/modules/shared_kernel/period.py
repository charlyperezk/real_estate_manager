from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class Period:
    year: int
    month: int

    def __post_init__(self):
        assert 1 <= self.month <= 12, "Month must be between 1 and 12"
        assert self.year <= 2025, "Year must be 2025 or earlier"

    def representation(self) -> str:
        return f"{self.month:02d}-{self.year}"

    @classmethod
    def from_str_format(cls, period: str) -> Period:
        month_str, year_str = period.split("-")
        return cls(year=int(year_str), month=int(month_str))
    
    @classmethod
    def get_current_period(cls) -> Period:
        now = datetime.now()
        return cls(
            year=now.year,
            month=now.month
        )