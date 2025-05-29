from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from ....shared_kernel.integration_events.after_finish_partner_finish_operation_partner import (
    OnAfterFinishPartnerFinishOperationPartner
)
from .. import partner_module
from ...domain.events import PartnershipWasFinished

@partner_module.handler(PartnershipWasFinished)
async def on_partner_finished(event: PartnershipWasFinished, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to PartnershipWasFinished -> Publishing " \
    "integration event OnAfterCreatePartnerCreateOperationPartner")
    
    await ctx.publish_async(
        OnAfterFinishPartnerFinishOperationPartner(
            partner_id=event.partner_id
        )
    )