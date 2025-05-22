from src.seedwork.domain.repositories import GenericRepository
from typing import List
from .entities import Strategy, GenericUUID

class StrategyRepository(GenericRepository[GenericUUID, Strategy]):
    def get_all(self) -> List[Strategy]:
        ...

    def get_strategies_by_property_id(self, property_id: GenericUUID) -> List[Strategy]:
        ...