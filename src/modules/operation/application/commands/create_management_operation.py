from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Fee, Money
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.entities import Operation, OperationType, AchievementType
from ...domain.repositories import OperationRepository
from ...domain.events import ManagementOperationWasStarted
from ....shared_kernel.integration_events.after_create_strategy_create_management_operation import (
    OnAfterCreateStrategyCreateManagementOperation
)

class CreateManagementOperation(Command):
    property_id: GenericUUID
    strategy_id: GenericUUID
    type: OperationType
    fee: Fee
    amount: Money
    description: str

@operation_module.handler(CreateManagementOperation)
async def create_management_operation(
        command: CreateManagementOperation,
        operation_repository: OperationRepository,
        logger: Logger
    ) -> Operation:
    
    logger.info("Creating management operation")

    operation = Operation(
        id=command.id,
        strategy_id=command.strategy_id,
        property_id=command.property_id,
        partner_id=GenericUUID(int=1),
        achievement_type=AchievementType.MANAGEMENT,
        type=command.type,
        fee=command.fee,
        amount=command.amount,
        description=command.description,
    )
        
    operation.register_event(        
        ManagementOperationWasStarted(
            operation_id=operation.id,
            property_id=operation.property_id,
            type=operation.type,
            status=operation.status,
            created_at=operation.created_at,
            description=operation.description,
        )
    )    

    operation_repository.add(entity=operation)

    return operation

# Integration Handler:
@operation_module.handler(OnAfterCreateStrategyCreateManagementOperation)
async def on_after_create_strategy_create_management_operation(
    command: OnAfterCreateStrategyCreateManagementOperation,
    ctx: TransactionContext
):
    await ctx.execute_async(
        CreateManagementOperation(
            id=command.id,
            strategy_id=command.strategy_id,
            property_id=command.property_id,
            type=command.type,
            fee=command.fee,
            amount=command.amount,
            description=command.description,
        )
    )