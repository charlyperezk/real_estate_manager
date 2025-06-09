from lato import TransactionContext
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.events import OperationStatusChangedToInProgress
from ....shared_kernel.integration_events.on_after_completed_partner_achievement import (
    OnAfterCompletedPartnerAchievement
)

@operation_module.handler(OperationStatusChangedToInProgress)
async def on_operation_in_progress(event: OperationStatusChangedToInProgress,
                    logger: Logger, ctx: TransactionContext) -> None:
    logger.info("Reacting to OperationStatusChangedToInProgress -> " \
    "Publishing integration event OnAfterCompletedPartnerAchievement")
    
    if event.partner_id != GenericUUID(int=1):
        await ctx.publish_async(
            OnAfterCompletedPartnerAchievement(
                achievement_type=event.achievement_type,
                partner_id=event.partner_id,
                revenue=event.revenue,
                period=event.period
            )
        )