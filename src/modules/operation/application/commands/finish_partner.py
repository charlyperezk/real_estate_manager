from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.repositories import OperationPartnerRepository
from ...domain.entities import Partner
from ....shared_kernel.integration_events.after_finish_partner_finish_operation_partner import (
    OnAfterFinishPartnerFinishOperationPartner
)

class FinishPartnership(Command):
    partner_id: GenericUUID

@operation_module.handler(FinishPartnership)
async def finish_partnership(
        command: FinishPartnership,
        operation_partner_repository: OperationPartnerRepository,
        logger: Logger
    ) -> Partner:
    
    logger.info("Updating partner status to finished")
    
    partner = operation_partner_repository.get_by_id(entity_id=command.partner_id)
    partner.finish()
    operation_partner_repository.persist(entity=partner)

    return partner

# Integration Handler:
@operation_module.handler(OnAfterFinishPartnerFinishOperationPartner)
async def on_after_finish_partner_finish_operation_partner(
        command: OnAfterFinishPartnerFinishOperationPartner,
        ctx: TransactionContext
    ):

    await ctx.execute_async(FinishPartnership(partner_id=command.partner_id))