from typing import Optional
from src.seedwork.domain.value_objects import GenericUUID, Fee, Money
from src.seedwork.domain.services import DomainService
from ...shared_kernel import AchievementType, OperationType
from .entities import Operation, RealStateOperation

class OperationConsistencyOrchestrator(DomainService):
    def __init__(self, rs_operation: RealStateOperation):
        self.rs_operation = rs_operation

    @staticmethod
    def create_management_operation(
        property_id: GenericUUID,
        strategy_id: GenericUUID,
        type: OperationType,
        fee: Fee,
        amount: Money,
        description: Optional[str] = None,
    ) -> Operation:
        return Operation(
            id=GenericUUID.next_id(),
            strategy_id=strategy_id,
            property_id=property_id,
            partner_id=GenericUUID(int=1),
            achievement_type=AchievementType.MANAGEMENT,
            type=type,
            fee=fee,
            amount=amount,
            description=description or "Management",
        )

    def register_achievement(self, achievement_type: AchievementType, partner_id: GenericUUID,
                              tier_fee: Fee, description: str) -> Operation:
        partner_share = self.rs_operation.calculate_partner_revenue(tier_partner=tier_fee)

        new_op = Operation(
            id = GenericUUID.next_id(),
            property_id=self.rs_operation.property_id,
            strategy_id=self.rs_operation.strategy_id,
            partner_id=partner_id,
            achievement_type=achievement_type,
            type=self.rs_operation.type,
            fee=tier_fee,
            amount=partner_share,
            description=description,
        )

        if achievement_type == AchievementType.CAPTURE:
            self.rs_operation.set_capture(new_op)
        elif achievement_type == AchievementType.CLOSE:
            self.rs_operation.set_close(new_op)
        else:
            raise ValueError("Achievement type no válido")

        return new_op