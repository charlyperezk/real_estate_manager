from lato import Query
from typing import List
from .. import strategy_module
from ...domain.repositories import StrategyRepository, Strategy

class GetAllStrategiesWithRenewAlert(Query):
    ...

@strategy_module.handler(GetAllStrategiesWithRenewAlert)
async def get_all_strategies_with_renew_alert(strategy_repository: StrategyRepository) -> List[Strategy]:
    return [st for st in strategy_repository.get_all() if st.within_renew_alert_threshold()]