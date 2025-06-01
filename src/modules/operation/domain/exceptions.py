from src.seedwork.domain.exceptions import DomainException
from src.seedwork.domain.value_objects import GenericUUID

class ConsistencyError(DomainException):
    def __init__(self, message: str = "Consistency error"):
        super().__init__(message)

    @classmethod
    def real_state_operation_already_exists(cls, strategy_id: GenericUUID):
        return cls(message=f"Real state operation for strategy {strategy_id} already exists")
    
    @classmethod
    def real_state_operation_not_found(cls, strategy_id: GenericUUID):
        return cls(message=f"Real state operation for strategy {strategy_id} not found")