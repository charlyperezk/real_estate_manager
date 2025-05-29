from src.seedwork.domain.value_objects import GenericUUID
from src.config.container import create_application, create_db_engine
from src.config.api_config import ApiConfig

from src.modules.partner.application.commands import CreatePartner
from src.modules.partner.application.queries import GetPartner
from src.modules.partner.domain.entities import Partner

app = create_application(create_db_engine(ApiConfig()))

async def life_cycle_strategy():
    partner: Partner = await app.execute_async(
        CreatePartner(
            name="Charly Perez Küper",
            user_id=GenericUUID.next_id(),
            )
        )

    partner_read: Partner = await app.execute_async(
        GetPartner(
                partner_id=partner.id
            )
        )

import asyncio
strategy = asyncio.run(life_cycle_strategy())