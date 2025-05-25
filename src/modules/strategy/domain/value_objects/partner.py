from dataclasses import dataclass
from enum import Enum
from typing import List
from . import Fee

class PartnerType(str, Enum):
    SELLER = "Seller"
    ASSOCIATE = "Associate"
    COLLECTOR = "Collector"

@dataclass
class Partner:
    fee: Fee
    type: PartnerType
    name: str

    @staticmethod
    def get_default_partner_types() -> List[str]:
        return [value.value for value in list(PartnerType)]
    