from typing import Optional
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Money
from src.seedwork.infrastructure.logging import Logger
from .. import strategy_module
from ...domain.entities import Fee, Strategy, OperationType, DateRange
from ...domain.repositories import StrategyRepository
from ...domain.events import StrategyWasCreated
from ...domain.service import StrategyService

class CreateStrategy(Command):
    property_id: GenericUUID
    exclusivity: bool
    fee: Fee
    period: DateRange
    type: OperationType
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
        service = StrategyService(strategies=strategies)
        service.strategy_can_be_register(strategy=strategy)
        
    strategy.register_event(
        StrategyWasCreated(
            strategy_id=strategy.id,
            property_id=strategy.property_id,
            period=strategy.period,
            type=strategy.type,
            price=strategy.price,
            fee=strategy.fee,
            deposit=strategy.deposit, # type: ignore
            terms_conditions=strategy.terms_conditions
        )
    )    

    strategy_repository.add(entity=strategy)
    return strategy