from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from ....shared_kernel.integration_events.after_create_partner_create_operation_partner import (
    OnAfterCreatePartnerCreateOperationPartner
)
from .. import partner_module
from ...domain.events import PartnerWasActivated

@partner_module.handler(PartnerWasActivated)
async def on_partner_activated(event: PartnerWasActivated, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to PartnerWasActivated -> " \
    "Publishing integration event OnAfterCreatePartnerCreateOperationPartner")
    
    await ctx.publish_async(
        OnAfterCreatePartnerCreateOperationPartner(
            partner_id=event.partner_id,
            user_id=event.user_id,
            status=event.status,
            partnership=event.partnership,
            type=event.type,
            name=event.name        
        )
    )