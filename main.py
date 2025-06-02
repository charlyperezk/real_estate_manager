from src.seedwork.domain.value_objects import GenericUUID, Money
from src.config.container import create_application, create_db_engine
from src.config.api_config import ApiConfig

from src.modules.partner.application.commands import CreatePartner, RegisterAchievement, RemoveAchievement
from src.modules.partner.application.queries import GetPartner
from src.modules.partner.domain.entities import Partner

from src.modules.shared_kernel import AchievementType, Period

app = create_application(create_db_engine(ApiConfig()))

async def life_cycle_strategy():
    partner: Partner = await app.execute_async(
        CreatePartner(
            name="Juan Perez",
            user_id=GenericUUID.next_id(),
            )
        )
    
    await app.execute_async(
        RegisterAchievement(
            partner_id=partner.id,
            achievement_type=AchievementType.CLOSE,
            revenue=Money(amount=450000),
            period=Period.get_current_period()
        )
    )

    await app.execute_async(
        RemoveAchievement(
            partner_id=partner.id,
            achievement_type=AchievementType.CLOSE,
            revenue=Money(amount=450000),
            period=Period.get_current_period()            
        )
    )

    partner_read: Partner = await app.execute_async(
        GetPartner(
                partner_id=partner.id
            )
        )

import asyncio
strategy = asyncio.run(life_cycle_strategy())