from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Money
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import Partner
from ...domain.repositories import PartnerRepository
from ...domain.service import PartnerAchievementRegistrator
from ....shared_kernel import AchievementType, Period
from ....shared_kernel.integration_events.on_after_completed_partner_achievement import (
    OnAfterCompletedPartnerAchievement
)

class RegisterAchievement(Command):
    partner_id: GenericUUID
    achievement_type: AchievementType
    revenue: Money
    period: Period

@partner_module.handler(RegisterAchievement)
async def register_achievement(command: RegisterAchievement, partner_repository: PartnerRepository,
                                logger: Logger) -> Partner:
    logger.info(f"Registering achievement and evaluating performance partner {command.partner_id}")

    partner = partner_repository.get_by_id(entity_id=command.partner_id)
    registrator = PartnerAchievementRegistrator(partner=partner)
    registrator.register_achievement(
        achievement_type=command.achievement_type,
        revenue=command.revenue,
        period=command.period
    )
    registrator.evaluate_performance()
    
    partner_repository.persist(entity=partner)
    return partner

# Integration Handler:
@partner_module.handler(OnAfterCompletedPartnerAchievement)
async def on_after_completed_partner_achievement(
    event: OnAfterCompletedPartnerAchievement,
    ctx: TransactionContext
):
    await ctx.execute_async(
        RegisterAchievement(
            partner_id=event.partner_id,
            achievement_type=event.achievement_type,
            revenue=event.revenue,
            period=event.period
        )
    )