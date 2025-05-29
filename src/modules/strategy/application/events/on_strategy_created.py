from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from ....shared_kernel.integration_events.after_create_strategy_create_management_operation import OnAfterCreateStrategyCreateManagementOperation
from .. import strategy_module
from ...domain.events import StrategyWasCreated

@strategy_module.handler(StrategyWasCreated)
async def on_strategy_created(event: StrategyWasCreated, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to StrategyWasCreated -> Publishing integration event OnAfterCreateStrategyCreateManagementOperation")
    
    await ctx.publish_async(
        OnAfterCreateStrategyCreateManagementOperation(
            property_id=event.property_id,
            strategy_id=event.strategy_id,
            description="Management",
            amount=event.price.calculate_fee(event.fee),
            fee=event.fee,
            type=event.type
        )
    )