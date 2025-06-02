from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Money
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import Partner
from ...domain.repositories import PartnerRepository
from ...domain.service import PartnerAchievementRegistrator
from ....shared_kernel import AchievementType
# from ....shared_kernel.integration_events.on_after_completed_partner_achievement import (
#     ...
# )

class RemoveAchievement(Command):
    partner_id: GenericUUID
    period: str
    achievement_type: AchievementType
    revenue: Money

@partner_module.handler(RemoveAchievement)
async def remove_achievement(command: RemoveAchievement, partner_repository: PartnerRepository, logger: Logger) -> Partner:
    logger.info(f"Removing achievement from period {command.period} and re-evaluating " \
                 "performance from partner {command.partner_id}")

    partner = partner_repository.get_by_id(entity_id=command.partner_id)
    registrator = PartnerAchievementRegistrator(partner=partner)
    registrator.remove_achievement(
        period=command.period, #TODO: Period check
        achievement_type=command.achievement_type,
        revenue=command.revenue
    )
    registrator.evaluate_performance()
    
    partner_repository.add(entity=partner)
    return partner

# Integration Handler:
# @partner_module.handler(...)
# async def on_after_X_remove_achievement(
#     event: ...,
#     ctx: TransactionContext
# ):
#     await ctx.execute_async(
#         RemoveAchievement(
#             period=event.period,
#             partner_id=event.partner_id,
#             achievement_type=event.achievement_type,
#             revenue=event.revenue
#         )
#     )