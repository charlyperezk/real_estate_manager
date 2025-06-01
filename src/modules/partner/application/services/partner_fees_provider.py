from src.seedwork.domain.value_objects import GenericUUID
from ...domain.repositories import PartnerRepository
from ...domain.service import PartnerEvaluator
from ....shared_kernel import AchievementType, OperationType

class PartnerFeesProvider:
    def __init__(self, repository: PartnerRepository, evaluator: PartnerEvaluator):
        self.repository = repository
        self.evaluator = evaluator

    def get_fee_for(self, partner_id: GenericUUID, achievement_type: AchievementType,
                     operation_type: OperationType) -> float:
        partner = self.repository.get_by_id(partner_id)
        fee_policy = self.evaluator.get_fee_policies(partner.tier)[achievement_type]
        return fee_policy.fees[operation_type]