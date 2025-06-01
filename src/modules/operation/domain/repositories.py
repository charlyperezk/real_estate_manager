from src.seedwork.domain.repositories import GenericRepository
from typing import List, Optional
from .entities import Operation, GenericUUID, RealStateOperation

class OperationRepository(GenericRepository[GenericUUID, Operation]):
    def get_all(self) -> List[Operation]:
        ...

    def has_real_state_operation_initialized(self, strategy_id: GenericUUID) -> bool:
        ...

    def get_real_state_operation(self, strategy_id: GenericUUID) -> RealStateOperation:
        ...