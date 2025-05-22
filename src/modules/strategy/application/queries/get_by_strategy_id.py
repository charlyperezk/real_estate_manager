from lato import Query
from src.seedwork.domain.value_objects import GenericUUID
from .. import strategy_module
from ...domain.repositories import StrategyRepository, Strategy

class GetStrategy(Query):
    strategy_id: GenericUUID

@strategy_module.handler(GetStrategy)
async def get_strategy(query: GetStrategy, strategy_repository: StrategyRepository) -> Strategy:
    return strategy_repository.get_by_id(query.strategy_id)