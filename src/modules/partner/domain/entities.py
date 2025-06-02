from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict
from src.seedwork.domain.value_objects import Money
from src.seedwork.domain.entities import GenericUUID, AggregateRoot
from .default_policies import POLICIES
from .value_objects import FeePolicy
from .enums import PartnerTier
from .targets_log import TargetsLog
from .performance import PartnerPerformance

from ...shared_kernel import (
    PartnershipStatus,
    AchievementType,
    Period
)
from .rules import (
    PartnershipStatusMustNotBeAlreadyActive,
    PartnershipStatusMustNotBeAlreadyDeactivated,
    PartnershipStatusMustNotBeBanned
)
from .events import (
    PartnerWasActivated,
    PartnerWasDeactivated,
    PartnerWasBanned,
    PartnerTierWasUpdated,
    PartnerAchievementWasRegistered,
    PartnerAchievementWasRemoved
)

@dataclass
class Partner(AggregateRoot):
    user_id: GenericUUID
    name: str
    tier: PartnerTier = field(default=PartnerTier.JUNIOR)
    fee_policies: Dict[AchievementType, FeePolicy] = field(default_factory=lambda: POLICIES[PartnerTier.JUNIOR])
    targets_log: TargetsLog = field(default_factory=TargetsLog)
    status: PartnershipStatus = field(default=PartnershipStatus.INACTIVE)
    created_at: datetime = field(default_factory=datetime.now)

    def set_tier_and_fee_policies(self, tier: PartnerTier, fee_policies: Dict[AchievementType, FeePolicy]) -> None:
        self.check_rule(PartnershipStatusMustNotBeBanned(status=self.status))

        self.tier = tier
        self.fee_policies = fee_policies
        self.register_event(
            PartnerTierWasUpdated(
                partner_id=self.id,
                tier=tier
            )
        )

    def get_targets_log(self) -> Dict[str, PartnerPerformance]:
        return self.targets_log.get_all()

    def get_performance_by_period(self, period: Period) -> PartnerPerformance:
        return self.targets_log.get_or_create_period_performance(period=period)

    def set_performance(self, period: Period, performance: PartnerPerformance) -> None:
        self.targets_log.persist(period=period, performance=performance)

    def register_achievement(self, achievement_type: AchievementType, 
                             period: Period, revenue_amount: Money) -> None:
        performance = self.get_performance_by_period(period=period)
        
        if achievement_type == AchievementType.CLOSE:
            performance.register_close(amount=revenue_amount)        
        elif achievement_type == AchievementType.CAPTURE:
            performance.register_capture(amount=revenue_amount)        
        
        self.targets_log.persist(period=period, performance=performance)
        
        self.register_event(
            PartnerAchievementWasRegistered(
                partner_id=self.id,
                performance=performance,
                period=period
            )
        )

    def remove_achievement(self, achievement_type: AchievementType, 
                             period: Period, revenue_amount: Money) -> None:
        performance = self.get_performance_by_period(period=period)
        
        if achievement_type == AchievementType.CLOSE:
            performance.remove_close(amount=revenue_amount)
        elif achievement_type == AchievementType.CAPTURE:
            performance.remove_capture(amount=revenue_amount)        
        
        self.targets_log.persist(period=period, performance=performance)
        
        self.register_event(
            PartnerAchievementWasRemoved(
                partner_id=self.id,
                performance=performance,
                period=period
            )
        )

    def activate(self) -> None:
        self.check_rule(PartnershipStatusMustNotBeAlreadyActive(status=self.status))
        
        self.status = PartnershipStatus.ACTIVE
        self.register_event(
            PartnerWasActivated(
                status=self.status,
                partner_id=self.id,
                user_id=self.user_id,
                name=self.name,
                tier=self.tier
            )
        )

    def deactivate(self) -> None:
        self.check_rule(PartnershipStatusMustNotBeAlreadyDeactivated(status=self.status))
        
        self.status = PartnershipStatus.INACTIVE
        self.register_event(
            PartnerWasDeactivated(
                status=self.status,
                partner_id=self.id,
                user_id=self.user_id,
                name=self.name,
                tier=self.tier
            )
        )

    def ban(self, review_operations: bool=True) -> None:
        self.check_rule(PartnershipStatusMustNotBeBanned(status=self.status))

        self.status = PartnershipStatus.BANNED
        self.register_event(
            PartnerWasBanned(
                status=self.status,
                partner_id=self.id,
                user_id=self.user_id,
                name=self.name,
                tier=self.tier,
                review_operations=review_operations
            )
        )