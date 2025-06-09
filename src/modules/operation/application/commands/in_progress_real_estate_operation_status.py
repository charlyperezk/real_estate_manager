from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.entities import RealEstateOperation
from ...domain.repositories import OperationRepository
from ...domain.exceptions import ConsistencyError
from ....shared_kernel.integration_events.on_after_strategy_completed import OnAfterStrategyCompleted

class SetRealEstateOperationInProgress(Command):
    strategy_id: GenericUUID

@operation_module.handler(SetRealEstateOperationInProgress)
async def set_real_estate_operation_in_progress(
        command: SetRealEstateOperationInProgress,
        operation_repository: OperationRepository,
        logger: Logger
    ) -> RealEstateOperation:
    
    logger.info(f"Setting Real Estate Operation with strategy_id {command.strategy_id} in progress")

    if not operation_repository.has_real_estate_operation_initialized(strategy_id=command.strategy_id):
        raise ConsistencyError.real_estate_operation_not_found(strategy_id=command.strategy_id)
    
    re_operation = operation_repository.get_real_estate_operation(strategy_id=command.strategy_id)
    re_operation.in_progress()
    
    for op in re_operation.operations:
        operation_repository.persist(entity=op)

    return re_operation

# Integration Handler:
@operation_module.handler(OnAfterStrategyCompleted)
async def on_strategy_completed_set_real_estate_operations_in_progress(
    event: OnAfterStrategyCompleted,
    ctx: TransactionContext
):
    await ctx.execute_async(
        SetRealEstateOperationInProgress(
            strategy_id=event.strategy_id
        )
    )