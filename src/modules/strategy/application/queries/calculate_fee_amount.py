from lato import Query
from .. import strategy_module
from ...domain.value_objects import Money, Fee

class CalculateFeeAmount(Query):
    money: Money
    fee: Fee

@strategy_module.handler(CalculateFeeAmount)
async def calculate_fee_amount(query: CalculateFeeAmount) -> float:
    return query.money.calculate_amount_discounting_fee(query.fee).amount