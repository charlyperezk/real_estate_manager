from lato import Query
from typing import List
from .. import strategy_module
from ...domain.repositories import StrategyRepository, Strategy

class GetAllStrategies(Query):
    ...

@strategy_module.handler(GetAllStrategies)
async def get_all_strategies(strategy_repository: StrategyRepository) -> List[Strategy]:
    return strategy_repository.get_all()