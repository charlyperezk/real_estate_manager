from typing import Optional, List, Dict
from src.seedwork.domain.value_objects import GenericUUID, Fee, Money, Currency
from src.seedwork.domain.services import DomainService
from ...shared_kernel import AchievementType, OperationType
from .entities import Operation, RealEstateOperation, OperationStatus

class OperationConsistencyOrchestrator(DomainService):
    def __init__(self, re_operation: RealEstateOperation):
        self.re_operation = re_operation

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
        partner_share = self.re_operation.calculate_partner_revenue(tier_partner=tier_fee)

        new_op = Operation(
            id = GenericUUID.next_id(),
            property_id=self.re_operation.property_id,
            strategy_id=self.re_operation.strategy_id,
            partner_id=partner_id,
            achievement_type=achievement_type,
            type=self.re_operation.type,
            fee=tier_fee,
            amount=partner_share,
            description=description,
        )

        if achievement_type == AchievementType.CAPTURE:
            self.re_operation.set_capture(new_op)
        elif achievement_type == AchievementType.CLOSE:
            self.re_operation.set_close(new_op)
        else:
            raise ValueError("Invalid achievement type")

        return new_op
    
class OperationsAnalytics(DomainService):
    def __init__(self, operations: List[Operation]):
        self.operations = operations

    def get_partners_revenue_sum_by_currency(self, currency: Currency) -> Dict[GenericUUID, Money]:
        dict_partner_id_revenue: Dict[GenericUUID, Money] = {}
        
        def is_within_the_scope(operation: Operation) -> bool:
            has_desired_status = operation.status in [
                OperationStatus.ACTIVE,
                OperationStatus.IN_PROGRESS,
                OperationStatus.PAID
            ]
            is_not_a_management_operation = operation.partner_id != GenericUUID(int=1)
            is_the_selected_currency = operation.amount.currency == currency

            return has_desired_status and is_not_a_management_operation and is_the_selected_currency

        operations = [op for op in self.operations if is_within_the_scope(op)]

        for operation in operations:
            if operation.partner_id in dict_partner_id_revenue:
                dict_partner_id_revenue[operation.partner_id] += operation.amount
            else:
                dict_partner_id_revenue[operation.partner_id] = operation.amount

        return dict_partner_id_revenue