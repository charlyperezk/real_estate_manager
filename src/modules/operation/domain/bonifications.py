from dataclasses import dataclass

@dataclass(frozen=True)
class Bonification:
    type: str
    description: str
    status: str
    value: float