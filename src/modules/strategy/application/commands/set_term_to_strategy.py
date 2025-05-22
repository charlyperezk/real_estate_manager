from typing import Optional
from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from .. import strategy_module
from ...domain.entities import Strategy
from ...domain.terms_and_conditions import Term, TermIdentifier
from ...domain.repositories import StrategyRepository

class SetTermToStrategy(Command):
    strategy_id: GenericUUID
    type: TermIdentifier
    description: str
    active: Optional[bool]

@strategy_module.handler(SetTermToStrategy)
async def set_term_to_strategy(command: SetTermToStrategy, strategy_repository: StrategyRepository) -> Strategy:
    strategy = strategy_repository.get_by_id(command.strategy_id)
    
    term = Term(
        type=command.type,
        description=command.description,
        active=command.active if command.active else True
    )
    strategy.register_term(term)
    strategy_repository.persist(strategy)
    
    return strategy