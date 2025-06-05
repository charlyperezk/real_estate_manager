from src.seedwork.domain.rules import BusinessRule
from .operation_status import OperationStatus
from ...shared_kernel import AchievementType

# Operation rules
class OperationMustNotBeCancelled(BusinessRule):
    status: OperationStatus

    _message = "Operation was cancelled"

    def is_broken(self) -> bool:
        return self.status == OperationStatus.CANCELLED
    
class OperationMustNotBeUnderReview(BusinessRule):
    status: OperationStatus

    _message = "Operation is under review"

    def is_broken(self) -> bool:
        return self.status == OperationStatus.UNDER_REVIEW
    
class AchievementTypeMustChange(BusinessRule):
    achievement_type: AchievementType
    actual_achievement_type: AchievementType

    _message = f"The provided achievement type is already setted"

    def is_broken(self) -> bool:
        return self.achievement_type == self.actual_achievement_type