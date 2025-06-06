from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Fee, Money
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.entities import Operation, OperationType
from ...domain.repositories import OperationRepository
from ...domain.events import RealEstateOperationWasInitialized
from ...domain.exceptions import ConsistencyError
from ...domain.service import OperationConsistencyOrchestrator
from ....shared_kernel.integration_events.on_after_activate_strategy import OnAfterActivateStrategy

class InitRealEstateOperation(Command):
    property_id: GenericUUID
    strategy_id: GenericUUID
    type: OperationType
    fee: Fee
    amount: Money

@operation_module.handler(InitRealEstateOperation)
async def init_real_estate_operation(
        command: InitRealEstateOperation,
        operation_repository: OperationRepository,
        logger: Logger
    ) -> Operation:
    
    logger.info(f"Initialiazing real state operation {command.type} for property {command.property_id}")

    if operation_repository.has_real_estate_operation_initialized(command.strategy_id):
        raise ConsistencyError.real_estate_operation_already_exists(strategy_id=command.strategy_id)

    management_operation = OperationConsistencyOrchestrator.create_management_operation(
        strategy_id=command.strategy_id,
        property_id=command.property_id,
        type=command.type,
        fee=command.fee,
        amount=command.amount,
    )
            
    management_operation.register_event(        
        RealEstateOperationWasInitialized(
            operation_id=management_operation.id,
            property_id=management_operation.property_id,
            type=management_operation.type,
            status=management_operation.status,
            created_at=management_operation.created_at,
            description=management_operation.description,
            revenue=management_operation.amount
        )
    )    

    operation_repository.add(entity=management_operation)

    return management_operation

# Integration Handler:
@operation_module.handler(OnAfterActivateStrategy)
async def on_after_create_strategy_init_real_estate_operation(
    event: OnAfterActivateStrategy,
    ctx: TransactionContext
):
    await ctx.execute_async(
        InitRealEstateOperation(
            id=event.id,
            strategy_id=event.strategy_id,
            property_id=event.property_id,
            type=event.type,
            fee=event.fee,
            amount=event.price,
        )
    )