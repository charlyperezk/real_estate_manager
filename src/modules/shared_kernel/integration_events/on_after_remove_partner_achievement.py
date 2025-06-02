from src.seedwork.domain.value_objects import GenericUUID, Money
from src.seedwork.application.events import IntegrationEvent
from .. import AchievementType
from .. import Period

class OnAfterRemovePartnerAchievement(IntegrationEvent):
    partner_id: GenericUUID
    period: Period
    achievement_type: AchievementType
    revenue: Money