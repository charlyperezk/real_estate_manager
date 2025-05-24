from lato import Query
from typing import List
from src.seedwork.domain.value_objects import GenericUUID
from .. import strategy_module
from ...domain.repositories import StrategyRepository

class CalculateStrategyFeeAmount(Query):
    strategy_id: GenericUUID

@strategy_module.handler(CalculateStrategyFeeAmount)
async def get_all_strategies_with_renew_alert(query: CalculateStrategyFeeAmount,
                                               strategy_repository: StrategyRepository) -> float:
    strategy = strategy_repository.get_by_id(query.strategy_id)
    return strategy.calculate_fee().amount