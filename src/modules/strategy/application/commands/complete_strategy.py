from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from .. import strategy_module
from ...domain.entities import Strategy
from ...domain.repositories import StrategyRepository

class CompleteStrategy(Command):
    strategy_id: GenericUUID

@strategy_module.handler(CompleteStrategy)
async def complete_strategy(command: CompleteStrategy, strategy_repository: StrategyRepository) -> Strategy:
    strategy = strategy_repository.get_by_id(command.strategy_id)
    strategy.mark_as_completed()
    strategy_repository.persist(strategy)
    
    return strategy