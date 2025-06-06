from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import strategy_module
from ...domain.repositories import StrategyRepository

class DiscontinueStrategy(Command):
    strategy_id: GenericUUID

@strategy_module.handler(DiscontinueStrategy)
async def discontinue_strategy(command: DiscontinueStrategy, strategy_repository: StrategyRepository,
                           logger: Logger) -> None:
    logger.info(f"Discontinuing strategy {command.strategy_id}")
    
    strategy = strategy_repository.get_by_id(entity_id=command.strategy_id)
    strategy.discontinue()
    strategy_repository.persist(entity=strategy)
    return