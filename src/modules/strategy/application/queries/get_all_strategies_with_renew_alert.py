from lato import Query
from typing import List
from .. import strategy_module
from ...domain.repositories import StrategyRepository, Strategy

class GetAllStrategiesWithRenewAlert(Query):
    ...

@strategy_module.handler(GetAllStrategiesWithRenewAlert)
async def get_all_strategies_with_renew_alert(strategy_repository: StrategyRepository) -> List[Strategy]:
    return list(filter(lambda strategie: strategie.is_in_renew_alert_period(), strategy_repository.get_all()))