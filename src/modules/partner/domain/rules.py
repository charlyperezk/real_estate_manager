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

class PartnershipStatusMustNotBeAlreadyDeactivated(BusinessRule):
    status: PartnershipStatus

    _message = "Partner is already deactivated"

    def is_broken(self) -> bool:
        return self.status == PartnershipStatus.INACTIVE

class PartnershipStatusMustNotBeBanned(BusinessRule):
    status: PartnershipStatus

    _message = "Partner is banned"

    def is_broken(self) -> bool:
        return self.status == PartnershipStatus.BANNED