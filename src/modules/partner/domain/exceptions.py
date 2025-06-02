from src.seedwork.domain.exceptions import DomainException
from ...shared_kernel import PartnershipStatus

class PartnerException(DomainException):
    def __init__(self, message: str = "Partner domain error"):
        super().__init__(message)

    @classmethod
    def without_permissions(cls, status: PartnershipStatus):
        return cls(f"Partner without permissions. PartnershipStatus {status}")