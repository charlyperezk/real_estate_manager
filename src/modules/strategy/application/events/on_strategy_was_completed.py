from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import strategy_module
from ...domain.events import StrategyWasCompleted
from ....shared_kernel.integration_events.on_after_strategy_completed import OnAfterStrategyCompleted

@strategy_module.handler(StrategyWasCompleted)
async def on_strategy_completed(event: OnAfterStrategyCompleted, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to StrategyWasCompleted -> " \
    "Publishing integration event OnAfterStrategyCompleted")
    
    await ctx.publish_async(
        OnAfterStrategyCompleted(
            strategy_id=event.strategy_id,
            price=event.price,
            fee=event.fee,
        )
    )