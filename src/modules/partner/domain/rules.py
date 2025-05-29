from ...shared_kernel import (
    PartnershipStatus,
)
from src.seedwork.domain.rules import BusinessRule

# Partner rules
class PartnershipStatusMustNotBeAlreadyActive(BusinessRule):
    status: PartnershipStatus

    _message = "Partner is already active"

    def is_broken(self) -> bool:
        return self.status == PartnershipStatus.ACTIVE

class PartnershipStatusMustNotBeBanned(BusinessRule):
    status: PartnershipStatus

    _message = "Partner is banned"

    def is_broken(self) -> bool:
        return self.status == PartnershipStatus.BANNED