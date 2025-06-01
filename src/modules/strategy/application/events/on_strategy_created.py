from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import strategy_module
from ...domain.events import StrategyWasCreated
from ....shared_kernel.integration_events.on_after_create_strategy import OnAfterCreateStrategy

@strategy_module.handler(StrategyWasCreated)
async def on_strategy_created(event: StrategyWasCreated, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to StrategyWasCreated -> " \
    "Publishing integration event OnAfterCreateStrategy")
    
    await ctx.publish_async(
        OnAfterCreateStrategy(
            property_id=event.property_id,
            strategy_id=event.strategy_id,
            price=event.price,
            fee=event.fee,
            type=event.type,
        )
    )