from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.events import PartnerWasActivated

@partner_module.handler(PartnerWasActivated)
async def on_partner_was_activated(event: PartnerWasActivated,
                    logger: Logger, ctx: TransactionContext) -> None:
    logger.info("Reacting to PartnerWasActivated -> " \
    "Publishing integration event OnAfterActivatePartner")
    