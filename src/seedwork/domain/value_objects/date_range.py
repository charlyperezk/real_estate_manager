from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from .value_objects import ValueObject

@dataclass(frozen=True)
class DateRange(ValueObject):
    start: datetime
    end: datetime

    def __post_init__(self):
        assert self.start < self.end, "Start date must be before the end date"

    @property
    def already_started(self) -> bool:
        return self.start < datetime.now()
    
    @property
    def finished(self) -> bool:
        return datetime.now() > self.end

    @property
    def on_going(self) -> bool:
        return self.already_started and not self.finished

    @property
    def days_to_start(self) -> int:
        _days_to_start = (self.start - datetime.now()).days
        return _days_to_start if _days_to_start else 0

    @property
    def days_left(self) -> int:
        return self.relative_date_days_left(datetime.now())

    @property
    def period_range_days(self) -> int:
        return (self.end - self.start).days

    @staticmethod
    def create_range_starting_now(end: datetime) -> DateRange:
        return DateRange(datetime.now(), end)

    @staticmethod
    def add_period_to_datetime(_from: datetime, **period: float) -> datetime:
        for key in period:
            if key not in {"days", "weeks"}:
                raise ValueError(f"Invalid key: It must be 'days' or 'weeks' ")
        return _from + timedelta(**period)

    @staticmethod
    def from_now_to(**period: float) -> DateRange:
        end_period_datetime = DateRange.add_period_to_datetime(_from=datetime.now(), **period)
        return DateRange.create_range_starting_now(end_period_datetime)

    def relative_date_days_left(self, date: datetime) -> int:
        return DateRange(date, self.end).period_range_days if not self.finished else 0

    def stopped(self) -> DateRange:
        return replace(self, end=datetime.now())

    def extended(self, **period: float) -> DateRange:
        new_end = DateRange.add_period_to_datetime(_from=self.end, **period)
        assert new_end > self.end, f"You are not extending the period. Last: {self.end} Passed: {new_end}"
        
        return replace(self, end=new_end)