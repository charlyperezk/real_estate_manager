from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.events import PartnerAchievementOperationRegistered
from ....shared_kernel.integration_events.on_after_register_partner_achievement import (
    OnAfterRegisterPartnerAchievement
)

@operation_module.handler(PartnerAchievementOperationRegistered)
async def on_register_partner_achievement(event: PartnerAchievementOperationRegistered,
                    logger: Logger, ctx: TransactionContext) -> None:
    logger.info("Reacting to PartnerAchievementOperationRegistered -> " \
    "Publishing integration event OnAfterRegisterPartnerAchievement")
    
    await ctx.publish_async(
        OnAfterRegisterPartnerAchievement(
            achievement_type=event.achievement_type,
            partner_id=event.partner_id,
            revenue=event.revenue
        )
    )