from dataclasses import dataclass, field, replace
from typing import List, Optional
from src.seedwork.domain.mixins import check_rule
from src.seedwork.domain.value_objects import GenericUUID
from .operation import Operation
from ....shared_kernel.status import OperationStatus
from ....shared_kernel.achievement_types import AchievementType

def auto_refresh_operations(method):
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.refresh_registered_operations_quantity()
        return result
    return wrapper

@dataclass
class Operations:
    operations: List[Operation] = field(default_factory=list)
    registered_operations: int = 0

    def refresh_registered_operations_quantity(self) -> None:
        self.registered_operations = len(self.get_operations())

    @auto_refresh_operations
    def register_operation(self, operation: Operation) -> None:
        assert not any(
            self.get_operations(achievement_type=operation.achievement_type)
        ), f"Operation of type {operation.achievement_type} is already in operations"
        
        self.operations.append(operation)

    @auto_refresh_operations
    def delete_operation(self, operation_id: GenericUUID) -> None:
        operation = self.get_operation_by_id(operation_id)
        self.operations = [op for op in self.operations if operation.id != operation_id ]

    @auto_refresh_operations
    def update_operation(self, operation_id: GenericUUID, **kwargs) -> None:
        operation = self.get_operation_by_id(operation_id)
        self.operations = [replace(op, **kwargs) if op.id == operation.id else op for op in self.operations]

    def get_operations(
            self,
            status: Optional[OperationStatus]=None,
            achievement_type: Optional[AchievementType]=None
    ) -> List[Operation]:
        operations = self.operations
        if status:
            operations = [operation for operation in operations if operation.status == status]
        if achievement_type:
            operations = [operation for operation in operations if operation.achievement_type == achievement_type]
        return self.operations

    def get_operation_by_id(self, operation_id: GenericUUID) -> Operation:
        operation = next((op for op in self.operations if op.id == operation_id))
        assert operation, "Operation not found"
        return operation