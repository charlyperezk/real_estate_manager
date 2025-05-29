from src.seedwork.domain.value_objects import GenericUUID, Currency, Money
from src.config.container import create_application, create_db_engine
from src.config.api_config import ApiConfig

from src.modules.strategy.application.commands import CreateStrategy, ActivateStrategy
from src.modules.strategy.application.queries import GetStrategy
from src.modules.strategy.application.commands.set_term_to_strategy import SetTermToStrategy
from src.modules.strategy.domain.entities import Fee, OperationType, DateRange

from src.modules.partner.application.commands import CreatePartner, SetPartnerFee
from src.modules.partner.application.queries import GetPartner
from src.modules.partner.domain.entities import Partnership, PartnerFee, PartnershipType, Partner

from src.modules.operation.application.commands import CreateManagementOperation
from src.modules.operation.domain.entities import Operation

rent_fee = Fee(value=15)
period = DateRange.from_now_to(weeks=2)
amount = Money(amount=450, currency=Currency.USD)
type = OperationType.RENT

app = create_application(create_db_engine(ApiConfig()))

async def life_cycle_strategy():
    # strategy = await app.execute_async(
    #     CreateStrategy(
    #         property_id=GenericUUID.next_id(),
    #         exclusivity=True,
    #         fee=rent_fee,
    #         period=period,
    #         type=type,
    #         price=amount,
    #         deposit=amount
    #     )
    # )

    # await app.execute_async(
    #     SetTermToStrategy(
    #         strategy_id=strategy.id,
    #         type="pets",
    #         description="Pets not allowed",
    #         active=True
    #     )
    # )
    
    # await app.execute_async(
    #     GetStrategy(
    #         strategy_id=strategy.id
    #     )
    # )

    await app.execute_async(
        ActivateStrategy(
            strategy_id=GenericUUID("b6ce513b-4184-4e63-b9c5-b3c5a80ab2ec")
        )
    )

    # await app.execute_async(
    #     CreatePartner(
    #         name="Charly Perez Küper",
    #         user_id=GenericUUID.next_id(),
    #         type=PartnershipType.SELLER
    #         )
    #     )

    # await app.execute_async(
    #     SetPartnerFee(
    #         partner_id=GenericUUID('0b45e34b-55e6-486b-a51d-b0a8459d9a42'),
    #         operation_type=OperationType.SELL,
    #         on_capture=10,
    #         on_close=10
    #     )
    # )
    # partner: Partner = await app.execute_async(GetPartner(partner_id=GenericUUID('0b45e34b-55e6-486b-a51d-b0a8459d9a42')))
    
    # operation: Operation = await app.execute_async(
    #     CreateManagementOperation(
    #         amount=Money(amount=45000, currency=Currency.USD),
    #         fee=Fee(value=10),
    #         description="Management",
    #         property_id=GenericUUID.next_id(),
    #         strategy_id=GenericUUID.next_id(),
    #         type=OperationType.SELL
    #     )
    # )


import asyncio
strategy = asyncio.run(life_cycle_strategy())