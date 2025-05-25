from src.seedwork.domain.entities import AggregateRoot
from dataclasses import dataclass
from .value_objects.superfice import Superfice

@dataclass
class Property(AggregateRoot):
    status: str
    total_superfice: Superfice
    cover_superfice: Superfice
    rooms: int
    bathrooms: int
    bedrooms: int
    parking_slots: int
    covered_parking_slots: int
    garden: bool
    longitude: str
    latitude: str
    address: str
    years_old: int
    condition: str
    type: str