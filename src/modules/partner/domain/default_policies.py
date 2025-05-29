from typing import Dict
from .enums.partner_tier import PartnerTier
from .value_objects import FeePolicy
from ...shared_kernel import OperationType, AchievementType

def instantiate_policy(rent_fee: float, sell_fee: float) -> FeePolicy:
    return FeePolicy(
        fees={
            OperationType.RENT: rent_fee,
            OperationType.SELL: sell_fee
        }
    )

POLICIES: Dict[PartnerTier, Dict[AchievementType, FeePolicy]] = {
    PartnerTier.JUNIOR: {
        AchievementType.CAPTURE: instantiate_policy(rent_fee=10, sell_fee=5),
        AchievementType.CLOSE: instantiate_policy(rent_fee=20, sell_fee=10),
    },
    PartnerTier.SENIOR: {
        AchievementType.CAPTURE: instantiate_policy(rent_fee=13, sell_fee=8),
        AchievementType.CLOSE: instantiate_policy(rent_fee=22, sell_fee=12),
    },
    PartnerTier.MASTER: {
        AchievementType.CAPTURE: instantiate_policy(rent_fee=15, sell_fee=10),
        AchievementType.CLOSE: instantiate_policy(rent_fee=24, sell_fee=14),
    },
}