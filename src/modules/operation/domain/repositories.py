from src.seedwork.domain.repositories import GenericRepository
from typing import List
from .entities import Operation, GenericUUID

class OperationRepository(GenericRepository[GenericUUID, Operation]):
    def get_all(self) -> List[Operation]:
        ...