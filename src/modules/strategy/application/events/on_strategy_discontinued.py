from lato import TransactionContext
from src.seedwork.infrastructure.logging import Logger
from .. import strategy_module
from ...domain.events import StrategyWasDiscontinued
from ....shared_kernel.integration_events.on_after_discontinue_strategy import OnAfterDiscontinueStrategy

@strategy_module.handler(StrategyWasDiscontinued)
async def on_strategy_created(event: StrategyWasDiscontinued, logger: Logger, ctx: TransactionContext):
    logger.info("Reacting to StrategyWasDiscontinued -> " \
    "Publishing integration event OnAfterDiscontinueStrategy")
    
    await ctx.publish_async(OnAfterDiscontinueStrategy(strategy_id=event.strategy_id))