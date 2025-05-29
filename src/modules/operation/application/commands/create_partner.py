from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.repositories import OperationPartnerRepository
from ...domain.entities import Partner
from ....shared_kernel import PartnershipStatus, Partnership, PartnershipType
from ....shared_kernel.integration_events.after_create_partner_create_operation_partner import (
    OnAfterCreatePartnerCreateOperationPartner
)

class CreatePartner(Command):
    partner_id: GenericUUID
    user_id: GenericUUID
    status: PartnershipStatus
    partnership: Partnership
    type: PartnershipType
    name: str

@operation_module.handler(CreatePartner)
async def create_partner(
        command: CreatePartner,
        operation_partner_repository: OperationPartnerRepository,
        logger: Logger
    ) -> Partner:
    
    logger.info("Creating partner")

    partner = Partner(
        id=command.partner_id,
        type=command.type,
        partnership=command.partnership,
        user_id=command.user_id,
        status=command.status,
        name=command.name
    )

    operation_partner_repository.add(entity=partner)
    return partner

# Integration Handler:
@operation_module.handler(OnAfterCreatePartnerCreateOperationPartner)
async def on_after_create_partner_create_operations_partner(
        command: OnAfterCreatePartnerCreateOperationPartner,
        ctx: TransactionContext
    ):
    await ctx.execute_async(
        CreatePartner(
            partner_id=command.partner_id,
            user_id=command.user_id,
            status=command.status,
            partnership=command.partnership,
            type=command.type,
            name=command.name        
        )
    )