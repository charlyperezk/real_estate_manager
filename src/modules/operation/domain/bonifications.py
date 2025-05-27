from dataclasses import dataclass

@dataclass(frozen=True)
class Bonification:
    scope: AchievementType
    description: str
    status: str
    value: float