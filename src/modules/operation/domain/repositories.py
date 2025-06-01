from src.seedwork.domain.repositories import GenericRepository
from typing import List
from .entities import Operation, GenericUUID, RealEstateOperation

class OperationRepository(GenericRepository[GenericUUID, Operation]):
    def get_all(self) -> List[Operation]:
        ...

    def has_real_estate_operation_initialized(self, strategy_id: GenericUUID) -> bool:
        ...

    def get_real_estate_operation(self, strategy_id: GenericUUID) -> RealEstateOperation:
        ...

    def get_operations_by_partner_id(self, partner_id: GenericUUID) -> List[Operation]:
        ...