from dataclasses import dataclass
from enum import Enum
from typing import List
from .value_objects import Fee
from src.seedwork.domain.entities import Entity

class PartnerType(str, Enum):
    SELLER = "Seller"
    ASSOCIATE = "Associate"
    COLLECTOR = "Collector"

@dataclass(frozen=True)
class Participation:
    fee: Fee
    type: PartnerType    

@dataclass
class Partner(Entity):
    participation: Participation

    @property
    def fee(self) -> Fee:
        return self.participation.fee

    @property
    def type(self) -> PartnerType:
        return self.participation.type

    @staticmethod
    def get_default_partner_types() -> List[str]:
        return [value.value for value in list(PartnerType)]
