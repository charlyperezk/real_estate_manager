from __future__ import annotations
from enum import Enum
from typing import Union, List
from dataclasses import dataclass, field, replace
from src.seedwork.domain.value_objects.value_objects import ValueObject

class TermType(Enum):
    REGISTERED_WORKER = "registered_worker"
    WARRANTY = "warranty"
    PETS = "pets"

    def __repr__(self) -> str:
        return str(self.value)

TermIdentifier = Union[TermType, str]

@dataclass(frozen=True, kw_only=True)
class Term(ValueObject):
    type: TermIdentifier
    active: bool = field(default=True)
    description: str = field(default="")

    @staticmethod
    def get_default_term_types() -> List[str]:
        return [value.value for value in list(TermType)]

    def activated(self) -> Term:
        assert not self.active, "Term is already activated"
        return replace(self, active=True)

    def deactivated(self) -> Term:
        assert self.active, "Term is already deactivated"
        return replace(self, active=False)
    
    def with_main_attributes_updated(self, active: bool, description: str) -> Term:
        return replace(self, active=active, description=description)