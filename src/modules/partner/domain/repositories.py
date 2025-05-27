from src.seedwork.domain.repositories import GenericRepository
from typing import List
from .entities import Partner, GenericUUID

class PartnerRepository(GenericRepository[GenericUUID, Partner]):
    def get_all(self) -> List[Partner]:
        ...