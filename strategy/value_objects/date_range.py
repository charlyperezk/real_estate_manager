from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import datetime, timedelta

@dataclass(frozen=True)
class DateRange:
    """
    Value object para utilidades comunes en un rango de fechas.

    Atributos:
    - start: la fecha en la cual comienza el rango.
    - end: la fecha en la cual termina el rango.

    """
    start: datetime
    end: datetime

    def __post_init__(self):
        assert self.start < self.end, "Start date must be before the end date"

    @property
    def valid(self) -> bool:
        """
        Retorna True si la fecha actual se encuentra dentro del rango, sino False.
        """
        return datetime.now() < self.end

    @property
    def days_left(self) -> int:
        """
        Retorna los días restante hasta el vencimiento del rango.
        """
        return self.relative_date_days_left(datetime.now())

    @property
    def period_range_days(self) -> int:
        return (self.end - self.start).days

    @staticmethod
    def create_range_starting_now(end: datetime) -> DateRange:
        return DateRange(datetime.now(), end)

    def relative_date_days_left(self, date: datetime) -> int:
        return DateRange(date, self.end).period_range_days if self.valid else 0

    def extended(self, **period: float) -> "DateRange":
        """
        Extiende el rango de fechas.

        Parámetros permitidos:
        - days: número de días a extender
        - weeks: número de semanas a extender
        """
        for key in period:
            if key not in {"days", "weeks"}:
                raise ValueError(f"Invalid key: {key}")
        return replace(self, end=self.end + timedelta(**period))