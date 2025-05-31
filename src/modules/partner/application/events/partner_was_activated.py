from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from ....shared_kernel.integration_events.on_after_activate_partner import (
    OnAfterActivatePartner
)
from .. import partner_module
from ...domain.events import PartnerWasActivated

@partner_module.handler(PartnerWasActivated)
async def on_partner_was_activated(event: PartnerWasActivated, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to PartnerWasActivated -> " \
    "Publishing integration event OnAfterActivatePartner")
    
    await ctx.publish_async(
        OnAfterActivatePartner(
            partner_id=event.partner_id,
            user_id=event.user_id,
            status=event.status,
            name=event.name        
        )
    )