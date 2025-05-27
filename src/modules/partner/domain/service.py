from typing import List, Optional
from dataclasses import dataclass
from src.seedwork.domain.services import DomainService
from src.seedwork.domain.mixins import check_rule
from src.seedwork.domain.rules import BusinessRule
from .entities import Partner

@dataclass
class PartnerService(DomainService):
    partners: List[Partner]
    registered_partners: int = 0

    def get_partners(self) -> List[Partner]:
        ...

    def refresh_registered_partners_quantity(self) -> None:
        self.registered_partners = len(self.get_partners())