from dataclasses import dataclass, field
from typing import List, Optional
from src.seedwork.domain.mixins import check_rule
from .rules import AchievementMustBeUnique
from .partner import Partner, AchievementType

@dataclass
class Partners:
    partners: List[Partner] = field(default_factory=list)

    @staticmethod
    def get_default_term_types() -> List[str]:
        return [value.value for value in list(AchievementType)]

    def get_partners(self, achievement_type: Optional[AchievementType]=None):
        partners = self.partners
        if type:
            partners = [partner for partner in partners if partner.type == achievement_type]
        return partners

    def add_partner(self, partner: Partner):
        check_rule(AchievementMustBeUnique(achievement_type=partner.type, partners=self.partners))        
        self.add_partner(partner)

    def delete_partner(self, achievement_type: AchievementType):
        partner = self.get_partners(achievement_type=achievement_type)
        assert partner, "Partner not found"
        self.partners = [partner for partner in self.partners if partner.type == achievement_type]

    def update_partner(self, partner: Partner):
        self.delete_partner(partner.type)
        self.add_partner(partner)