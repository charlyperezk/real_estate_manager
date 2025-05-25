from typing import List, Optional
from dataclasses import dataclass
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.domain.services import DomainService
from src.seedwork.domain.mixins import check_rule
from src.seedwork.domain.rules import BusinessRule
from .entities import Strategy, StrategyType, StrategyStatus

class StrategyMustBeUnique(BusinessRule):
    strategy_type: str
    strategies: List[Strategy]

    _message = "Strategy type already exists"

    def is_broken(self) -> bool:
        return any((strategy.type == self.strategy_type for strategy in self.strategies))

@dataclass
class StrategyService(DomainService):
    property_id: GenericUUID
    strategies: List[Strategy]
    registered_strategies: int = 0

    def get_strategies(
            self,
            accepted: bool=False,
            status: Optional[StrategyStatus]=None,
            type: Optional[StrategyType]=None
        ):
        result = self.strategies
        if accepted:
            result = list(filter(lambda strategy: strategy.accepted == status, result))
        if status:  
            result = list(filter(lambda strategy: strategy.status == status, result))
        if type:
            result = list(filter(lambda strategy: strategy.status == status, result))
        return result    
    
    def refresh_registered_strategies_quantity(self) -> None:
        self.registered_strategies = len(self.get_strategies())

    def any_rent_strategy_exist(self) -> bool:
        return any(self.get_strategies(type=StrategyType.RENT))

    def any_sell_strategy_exist(self) -> bool:
        return any(self.get_strategies(type=StrategyType.SELL))

    def any_strategy_accepted(self) -> bool:
        return any(self.get_strategies(accepted=True))

    def has_both_strategies_registered(self) -> bool:
        return self.any_rent_strategy_exist() and self.any_sell_strategy_exist()

    def strategy_can_be_register(self, strategy: Strategy):        
        check_rule(
            StrategyMustBeUnique(
                strategy_type=strategy.type,
                strategies=self.strategies
            )
        )        
        self.strategies.append(strategy)
        self.refresh_registered_strategies_quantity()