from __future__ import annotations
from typing import Dict
from dataclasses import dataclass
from ....shared_kernel import OperationType

@dataclass
class FeePolicy:
    fees: Dict[OperationType, float]

    def as_dict(self) -> Dict[OperationType, float]:
        return {
            op_type: pct
            for op_type, pct in self.fees.items()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> FeePolicy:
        return cls(
            fees={
                OperationType(op_type_str): float(pct)
                for op_type_str, pct in data.items()
            }
        )