from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.repositories import OperationRepository
from ....shared_kernel.integration_events.on_after_discontinue_strategy import OnAfterDiscontinueStrategy

class SetRealEstateOperationUnderReview(Command):
    strategy_id: GenericUUID

@operation_module.handler(SetRealEstateOperationUnderReview)
async def set_real_estate_operation_under_review(
    command: SetRealEstateOperationUnderReview,
    operation_repository: OperationRepository,
    logger: Logger
) -> None:
    logger.info(f"Setting Real Estate Operation with strategy_id {command.strategy_id} under review")
    
    re_operation = operation_repository.get_real_estate_operation(
        strategy_id=command.strategy_id
    )
    re_operation.under_review()
    
    for op in re_operation.operations:
        operation_repository.persist(entity=op)

    logger.info(f"{len(re_operation.operations)} operations were modified")


@operation_module.handler(OnAfterDiscontinueStrategy)
async def on_after_discontinue_strategy(
    event: OnAfterDiscontinueStrategy,
    ctx: TransactionContext
):
    await ctx.execute_async(
        SetRealEstateOperationUnderReview(
            strategy_id=event.strategy_id
        )
    )