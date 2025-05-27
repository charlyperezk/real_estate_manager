from src.seedwork.domain.value_objects import GenericUUID, Currency, Money
from src.config.container import create_application, create_db_engine
from src.config.api_config import ApiConfig

from src.modules.strategy.application import strategy_module
from src.modules.strategy.application.commands.create_strategy import CreateStrategy
from src.modules.strategy.application.queries import GetStrategy
from src.modules.strategy.application.commands.set_term_to_strategy import SetTermToStrategy
from src.modules.strategy.domain.entities import Fee, OperationType, DateRange

rent_fee = Fee(value=15)
period = DateRange.from_now_to(weeks=2)
amount = Money(amount=450, currency=Currency.USD)
type = OperationType.RENT

app = create_application(create_db_engine(ApiConfig()))
app.include_submodule(strategy_module)

async def life_cycle_strategy():
    strategy = await app.execute_async(
        CreateStrategy(
            property_id=GenericUUID.next_id(),
            exclusivity=True,
            fee=rent_fee,
            period=period,
            type=type,
            price=amount,
            deposit=amount
        )
    )

    await app.execute_async(
        SetTermToStrategy(
            strategy_id=strategy.id,
            type="pets",
            description="Pets not allowed",
            active=True
        )
    )
    
    await app.execute_async(
        GetStrategy(
            strategy_id=strategy.id
        )
    )

import asyncio
strategy = asyncio.run(life_cycle_strategy())