from lato import Query
from typing import List, Optional, Dict
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.repositories import OperationRepository
from ...domain.entities import RealEstateOperation, Operation
from ...domain.operation_status import OperationStatus

class GetAllRealEstateOperations(Query):
    status: Optional[OperationStatus]=None

@operation_module.handler(GetAllRealEstateOperations)
async def get_real_estate_operation(
        query: GetAllRealEstateOperations,
        operation_repository: OperationRepository,
        logger: Logger
    ) -> List[RealEstateOperation]:
    logger.info(f"Retrieving all real estate operations")
    
    operations = operation_repository.get_all()
    grouped_operations: Dict[GenericUUID, List[Operation]] = {}
    
    for op in operations:
        if op.strategy_id in grouped_operations:
            grouped_operations[op.strategy_id].append(op)
        else:
            grouped_operations[op.strategy_id] = [op]

    re_operations = [RealEstateOperation.from_operations(operations=ops) for
                      ops in grouped_operations.values()]

    if query.status:
        return [re_op 
                for re_op in re_operations if all(
                re_op.map_operations(func=lambda op: op.status == query.status))
            ]
    
    return re_operations