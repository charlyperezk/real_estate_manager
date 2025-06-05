from lato import Query
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.repositories import OperationRepository
from ...domain.entities import RealEstateOperation

class GetRealEstateOperation(Query):
    strategy_id: GenericUUID

@operation_module.handler(GetRealEstateOperation)
async def get_real_estate_operation(
        query: GetRealEstateOperation,
        operation_repository: OperationRepository,
        logger: Logger
    ) -> RealEstateOperation:
    logger.info(f"Retrieving real estate operation from strategy {query.strategy_id}")
    
    assert operation_repository.has_real_estate_operation_initialized(
        strategy_id=query.strategy_id
    ), "Strategy doesn't have a real estate operation initialized"
    
    operations = operation_repository.get_operations_by_strategy_id(strategy_id=query.strategy_id)
    
    return RealEstateOperation.from_operations(operations=operations)