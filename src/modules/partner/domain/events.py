from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.domain.events import DomainEvent
from .enums import PartnerTier
from ...shared_kernel import PartnershipStatus
from .performance import PartnerPerformance

class PartnerCreated(DomainEvent):
    ...

class PartnerWasActivated(DomainEvent):
    partner_id: GenericUUID
    user_id: GenericUUID
    status: PartnershipStatus
    tier: PartnerTier
    name: str

class PartnerWasBanned(PartnerWasActivated):
    ...

class PartnerTierWasUpdated(DomainEvent):
    partner_id: GenericUUID
    tier: PartnerTier

class PartnerAchievementWasRegistered(DomainEvent):
    partner_id: GenericUUID
    performance: PartnerPerformance