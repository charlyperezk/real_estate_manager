from .. import strategy_module
from src.seedwork.infrastructure.logging import Logger
from ...domain.events import StrategyWasActivated

@strategy_module.handler(StrategyWasActivated)
def on_strategy_activated(event: StrategyWasActivated, logger: Logger):
    logger.info("Greetings from strategy activated event handler")