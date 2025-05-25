from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from .. import strategy_module
from ...domain.value_objects import Fee
from ...domain.entities import Strategy
from ...domain.partners import Partner, PartnerType
from ...domain.repositories import StrategyRepository

class SetPartnerToStrategy(Command):
    strategy_id: GenericUUID
    type: PartnerType
    fee: Fee
    name: str

@strategy_module.handler(SetPartnerToStrategy)
async def set_term_to_strategy(command: SetPartnerToStrategy, strategy_repository: StrategyRepository) -> Strategy:
    strategy = strategy_repository.get_by_id(command.strategy_id)

    partner = Partner(
        type=command.type,
        fee=command.fee,
        name=command.name
    )
    strategy.add_partner(partner)
    strategy_repository.persist(strategy)
    
    return strategy