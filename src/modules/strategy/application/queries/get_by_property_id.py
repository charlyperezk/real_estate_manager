from lato import Query
from typing import List
from src.seedwork.domain.value_objects import GenericUUID
from .. import strategy_module
from ...domain.repositories import StrategyRepository, Strategy

class GetStrategiesByPropertyId(Query):
    property_id: GenericUUID

@strategy_module.handler(GetStrategiesByPropertyId)
async def get_strategies_by_property_id(query: GetStrategiesByPropertyId, strategy_repository: StrategyRepository) -> List[Strategy]:
    return strategy_repository.get_strategies_by_property_id(query.property_id)