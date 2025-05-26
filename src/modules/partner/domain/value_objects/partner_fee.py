from __future__ import annotations
from dataclasses import dataclass, replace
from ..operation_types import OperationType

@dataclass(frozen=True)
class PartnerFee:
    operation_type: OperationType
    on_capture: float
    on_close: float