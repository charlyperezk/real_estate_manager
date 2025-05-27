from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from .. import strategy_module
from ...domain.entities import Strategy, TermIdentifier
from ...domain.repositories import StrategyRepository

class DeleteTermFromStrategy(Command):
    strategy_id: GenericUUID
    identifier: TermIdentifier

@strategy_module.handler(DeleteTermFromStrategy)
async def delete_term_from_strategy(command: DeleteTermFromStrategy, strategy_repository: StrategyRepository) -> Strategy:
    strategy = strategy_repository.get_by_id(command.strategy_id)
    strategy.delete_term(term_type=command.identifier)
    strategy_repository.persist(strategy)
    
    return strategy