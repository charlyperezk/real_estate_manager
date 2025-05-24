from typing import Optional
from lato import TransactionContext
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import strategy_module
from ...domain.entities import Fee, Strategy, StrategyType, DateRange
from ...domain.value_objects.money import Money
from ...domain.repositories import StrategyRepository
from ...domain.events import StrategyWasActivated
from ...domain.service import StrategyService

class CreateStrategy(Command):
    property_id: GenericUUID
    exclusivity: bool
    fee: Fee
    period: DateRange
    type: StrategyType
    price: Money
    deposit: Optional[Money]

@strategy_module.handler(CreateStrategy)
async def create_strategy(command: CreateStrategy, strategy_repository: StrategyRepository, logger: Logger) -> Strategy:
    logger.info("Creating strategy")
    
    strategy = Strategy(
        id=command.id,
        property_id=command.property_id,
        exclusivity=command.exclusivity,
        fee=command.fee,
        period=command.period,
        type=command.type,
        price=command.price,
        deposit=command.deposit if command.deposit else Money(amount=0, currency=command.price.currency)
    )

    strategies = strategy_repository.get_strategies_by_property_id(property_id=command.property_id)
    if strategies:
        service = StrategyService(property_id=command.property_id, strategies=strategies)
        service.strategy_can_be_register(strategy=strategy)
        
    strategy.register_event(
        StrategyWasActivated(
            id=command.id,
            property_id=command.property_id,
            period=command.period,
            type=command.type,
            price=command.price,
            deposit=command.deposit if command.deposit else Money(amount=0, currency=command.price.currency),
            terms_conditions=strategy.terms_conditions
        )
    )    

    strategy_repository.add(entity=strategy)

    return strategy