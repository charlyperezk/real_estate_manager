from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.entities import Operation
from ...domain.repositories import OperationRepository
from ...domain.operation_status import OperationStatus
from ....shared_kernel.integration_events.on_after_partner_banned import OnAfterPartnerBanned

class ProcessPartnerBanned(Command):
    partner_id: GenericUUID
    review_operations: bool

@operation_module.handler(ProcessPartnerBanned)
async def set_partner_achievements_under_review(
    command: ProcessPartnerBanned,
    operation_repository: OperationRepository,
    logger: Logger
) -> None:
    if command.review_operations:
        logger.info(f"Marking partner operations as 'Under review' → {command.partner_id}")

    partner_operations: list[Operation] = operation_repository.get_operations_by_partner_id(
        partner_id=command.partner_id
    )

    partner_operations_to_update = [
        op for op in partner_operations
        if op.status in [OperationStatus.ACTIVE, OperationStatus.IN_PROGRESS]
    ]

    for operation in partner_operations_to_update:
        if command.review_operations: 
            operation.under_review()
            logger.info(f"Updated {len(partner_operations_to_update)} operations to UNDER_REVIEW")
        
        operation.description = "Partner was banned"
        operation_repository.persist(operation)


@operation_module.handler(OnAfterPartnerBanned)
async def on_after_partner_banned(
    event: OnAfterPartnerBanned,
    ctx: TransactionContext
):
    await ctx.execute_async(
        ProcessPartnerBanned(
            partner_id=event.partner_id,
            review_operations=event.review_operations
        )
    )