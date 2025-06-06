from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.application.exceptions import ApplicationException

class RealEstateOperationError(ApplicationException):
    def __init__(self, message: str="Real estate operation error"):
        super().__init__(message)

    @classmethod
    def real_estate_operation_not_found(cls, strategy_id: GenericUUID):
        return cls(
            message=f"Strategy {strategy_id} doesn't have a real estate operation initialized"
        )