from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Money
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import Partner
from ...domain.repositories import PartnerRepository
from ...domain.service import PartnerAchievementRegistrator
from ....shared_kernel import AchievementType
from ....shared_kernel.integration_events.on_after_register_partner_achievement import (
    OnAfterRegisterPartnerAchievement
)

class RegisterAchievement(Command):
    partner_id: GenericUUID
    achievement_type: AchievementType
    revenue: Money

@partner_module.handler(RegisterAchievement)
async def register_achievement(command: RegisterAchievement, partner_repository: PartnerRepository, logger: Logger) -> Partner:
    logger.info(f"Registering achievement and evaluating performance partner {command.partner_id}")

    partner = partner_repository.get_by_id(entity_id=command.partner_id)
    registrator = PartnerAchievementRegistrator(partner=partner)
    registrator.register_achievement(
        achievement_type=command.achievement_type,
        revenue=command.revenue
    )
    registrator.evaluate_performance()
    
    partner_repository.add(entity=partner)
    return partner

# Integration Handler:
@partner_module.handler(OnAfterRegisterPartnerAchievement)
async def on_after_register_partner_achievement(
    event: OnAfterRegisterPartnerAchievement,
    ctx: TransactionContext
):
    await ctx.execute_async(
        RegisterAchievement(
            partner_id=event.partner_id,
            achievement_type=event.achievement_type,
            revenue=event.revenue
        )
    )