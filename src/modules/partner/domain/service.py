from typing import Dict, List
from .entities import PartnerPerformance, Partner
from .value_objects import FeePolicy
from .enums import PartnerTier
from .default_policies import POLICIES
from ...shared_kernel import AchievementType, Period
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

    def register_achievement(self, achievement_type: AchievementType, 
                             revenue: Money, period: Period):
        self.partner.register_achievement(
            achievement_type=achievement_type,
            period=period,
            revenue_amount=revenue
        )

    def remove_achievement(self, achievement_type: AchievementType, 
                             revenue: Money, period: Period):
        self.partner.remove_achievement(
            achievement_type=achievement_type,
            period=period,
            revenue_amount=revenue
        )

    def evaluate_performance(self, period: Period=Period.get_current_period()) -> None:
        performance = self.partner.get_performance_by_period(period=period)
        evaluator = PartnerEvaluator()
        reached_tier = evaluator.determine_tier(performance=performance)
        
        if reached_tier != self.partner.tier:
            fee_policies = evaluator.get_fee_policies(tier=reached_tier)
            self.partner.set_tier_and_fee_policies(tier=reached_tier, fee_policies=fee_policies)

class PartnersPerformanceInsights(DomainService):
    def __init__(self, partners: List[Partner]) -> None:
        self.partners = partners

    def order_by_closes(self, period: Period=Period.get_current_period()) -> List[Partner]:
        def get_closes(partner: Partner) -> int:
            return partner.get_performance_by_period(period=period).operations_closed
        
        sorted_partners = sorted(self.partners.copy(), key=get_closes)
        return sorted_partners
    
    def order_by_captures(self, period: Period=Period.get_current_period()) -> List[Partner]:
        def get_captures(partner: Partner) -> int:
            return partner.get_performance_by_period(period=period).properties_captured
        
        sorted_partners = sorted(self.partners.copy(), key=get_captures)
        return sorted_partners
        
    def order_by_revenue_generated(self, period: Period=Period.get_current_period()) -> List[Partner]:
        def get_revenue_generated(partner: Partner) -> float:
            return partner.get_performance_by_period(period=period).revenue_generated.amount
        
        sorted_partners = sorted(self.partners.copy(), key=get_revenue_generated)
        return sorted_partners