from src.seedwork.domain.exceptions import DomainException
from src.seedwork.domain.value_objects import GenericUUID
from ...shared_kernel import AchievementType

class ConsistencyError(DomainException):
    def __init__(self, message: str = "Consistency error"):
        super().__init__(message)

    @classmethod
    def real_estate_operation_already_exists(cls, strategy_id: GenericUUID):
        return cls(message=f"Real state operation for strategy {strategy_id} already exists")
    
    @classmethod
    def real_estate_operation_not_found(cls, strategy_id: GenericUUID):
        return cls(message=f"Real state operation for strategy {strategy_id} not found")

    @classmethod
    def valid_achievement_operation_already_setted(cls, achievement_type: AchievementType):
        return cls(message=f"Valid {achievement_type} can't be overwritten")
    
    @classmethod
    def operation_with_wrong_achievement_type_received(cls, desired_achievement_type: AchievementType):
        return cls(message=f"You must pass a {desired_achievement_type} operation")

    @classmethod
    def management_operation_not_found(cls):
        return cls(message=f"Management operation not found")

    @classmethod
    def foreign_operations_found(cls):
        return cls(message=f"All operations must belong to the same strategy")