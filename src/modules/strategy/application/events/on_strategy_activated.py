from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import strategy_module
from ...domain.events import StrategyWasActivated
from ....shared_kernel.integration_events.on_after_activate_strategy import OnAfterActivateStrategy

@strategy_module.handler(StrategyWasActivated)
async def on_strategy_created(event: StrategyWasActivated, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to StrategyWasActivated -> " \
    "Publishing integration event OnAfterActivateStrategy")
    
    await ctx.publish_async(
        OnAfterActivateStrategy(
            property_id=event.property_id,
            strategy_id=event.strategy_id,
            price=event.price.calculate_fee(fee=event.fee),
            fee=event.fee,
            type=event.type,
        )
    )