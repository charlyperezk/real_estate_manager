from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.events import PartnerWasBanned
from ....shared_kernel.integration_events.on_after_partner_banned import OnAfterPartnerBanned

@partner_module.handler(PartnerWasBanned)
async def on_partner_banned(event: PartnerWasBanned, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to PartnerWasBanned -> Publishing " \
    "integration event OnAfterPartnerBanned")
    
    await ctx.publish_async(
        OnAfterPartnerBanned(
            partner_id=event.partner_id,
            review_operations=event.review_operations
        )
    )