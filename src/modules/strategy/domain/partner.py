from dataclasses import dataclass
from enum import Enum
from typing import List
from src.seedwork.domain.entities import Entity

class AchievementType(str, Enum):
    CLOSE = "close"
    CAPTURE = "associate"

@dataclass
class Partner(Entity):
    achievement_type: AchievementType

    @property
    def type(self) -> AchievementType:
        return self.achievement_type    

    @staticmethod
    def get_default_partner_types() -> List[str]:
        return [value.value for value in list(AchievementType)]
