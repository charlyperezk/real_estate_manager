from __future__ import annotations
from typing import Union, List
from dataclasses import dataclass
from enum import Enum

class TermType(Enum):
    REGISTERED_WORKER = "registered_worker"
    WARRANTY = "warranty"
    PETS = "pets"

TermIdentifier = Union[TermType, str]

@dataclass(frozen=True, kw_only=True)
class Term:
    type: TermIdentifier
    description: str
    active: bool

    @staticmethod
    def get_default_term_types() -> List[str]:
        return TermType._member_names_