from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.events import PartnerWasBanned

@partner_module.handler(PartnerWasBanned)
async def on_partner_finished(event: PartnerWasBanned, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to PartnerWasBanned -> Publishing " \
    "integration event OnAfterCreatePartnerCreateOperationPartner")
    ...