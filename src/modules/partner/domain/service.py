from typing import Dict
from .entities import PartnerPerformance, Partner
from .value_objects import FeePolicy
from .enums import PartnerTier
from .default_policies import POLICIES
from .utils import current_period
from ...shared_kernel import AchievementType
from src.seedwork.domain.value_objects import Money
from src.seedwork.domain.services import DomainService

class PartnerEvaluator(DomainService):
    def __init__(self, fee_policies: Dict[PartnerTier, Dict[AchievementType, FeePolicy]]=POLICIES) -> None:
        self.policies = fee_policies

    def determine_tier(self, performance: PartnerPerformance) -> PartnerTier:
        if performance.revenue_generated.amount > 25_000:
            return PartnerTier.MASTER
        elif performance.revenue_generated.amount > 7_500:
            return PartnerTier.SENIOR
        else:
            return PartnerTier.JUNIOR

    def get_fee_policies(self, tier: PartnerTier) -> Dict[AchievementType, FeePolicy]:
        return self.policies[tier]
        
class PartnerAchievementRegistrator(DomainService):
    def __init__(self, partner: Partner) -> None:
        self.partner = partner

    def register_achievement(self, achievement_type: AchievementType, revenue: Money):
        period = current_period()
        self.partner.register_achievement(
            achievement_type=achievement_type,
            period=period,
            revenue_amount=revenue
        )

    def remove_achievement(self, period: str, achievement_type: AchievementType, revenue: Money):
        performance = self.partner.get_performance_by_period(period=period)

        if achievement_type == AchievementType.CLOSE:
            performance.remove_close(amount=revenue)
        elif achievement_type == AchievementType.CAPTURE:
            performance.remove_capture(amount=revenue)

        self.partner.set_performance(period=period, performance=performance)

    def evaluate_performance(self) -> None:
        period = current_period()
        performance = self.partner.get_performance_by_period(period=period)
        evaluator = PartnerEvaluator()
        reached_tier = evaluator.determine_tier(performance=performance)
        
        if reached_tier != self.partner.tier:
            fee_policies = evaluator.get_fee_policies(tier=reached_tier)
            self.partner.set_tier_and_fee_policies(tier=reached_tier, fee_policies=fee_policies)
