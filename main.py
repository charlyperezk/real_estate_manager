import uuid

from src.seedwork.domain.value_objects import GenericUUID
from src.config.container import create_application, create_db_engine
from src.config.api_config import ApiConfig

from src.modules.strategy.application import strategy_module
from src.modules.strategy.application.commands.create_strategy import CreateStrategy
from src.modules.strategy.application.queries.get_by_strategy_id import GetStrategy
from src.modules.strategy.application.commands.set_term_to_strategy import SetTermToStrategy
from src.modules.strategy.domain.entities import Fee, Term, Strategy, StrategyStatus, StrategyType, DateRange
from src.modules.strategy.domain.value_objects.money import Currency, Money
from src.modules.strategy.domain.terms_and_conditions import TermType

sell_fee = Fee(value=15)
period = DateRange.from_now_to(weeks=2)
amount = Money(amount=450, currency=Currency.USD)
type = StrategyType.RENT

app = create_application(create_db_engine(ApiConfig()))
app.include_submodule(strategy_module)

async def life_cycle_strategy():
    strategy = await app.execute_async(
        CreateStrategy(
            property_id=GenericUUID.next_id(),
            exclusivity=True,
            fee=sell_fee,
            period=period,
            type=type,
            price=amount,
            deposit=amount
        )
    )
    return strategy

async def set_term_to_strategy(strategy_id):
    await app.execute_async(
        SetTermToStrategy(
            strategy_id=strategy_id,
            type="pets",
            description="Pets not allowed",
            active=True
        )
    )
    
async def get_strategy_created(strategy_id):
    strategy_obtained = await app.execute_async(
        GetStrategy(
            strategy_id=strategy_id
        )
    )

    return get_strategy_created

import asyncio
strategy = asyncio.run(life_cycle_strategy())
asyncio.run(set_term_to_strategy(strategy.id))
asyncio.run(get_strategy_created(strategy.id))
