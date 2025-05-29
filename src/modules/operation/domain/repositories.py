from src.seedwork.domain.repositories import GenericRepository
from typing import List
from .entities import Operation, Partner, GenericUUID

class OperationRepository(GenericRepository[GenericUUID, Operation]):
    def get_all(self) -> List[Operation]:
        ...

class OperationPartnerRepository(GenericRepository[GenericUUID, Partner]):
    def get_all(self) -> List[Operation]:
        ...