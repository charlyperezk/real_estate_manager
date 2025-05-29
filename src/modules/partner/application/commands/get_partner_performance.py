from typing import Optional, List
from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import PartnerPerformance
from ...domain.repositories import PartnerRepository

class GetPartnerPerformance(Command):
    partner_id: GenericUUID
    period: Optional[str] = None

@partner_module.handler(GetPartnerPerformance)
async def get_performance(command: GetPartnerPerformance, partner_repository: PartnerRepository,
                          logger: Logger) -> List[PartnerPerformance]:
    logger.info(f"Retrieving performance from partner with id {command.partner_id}")
    partner = partner_repository.get_by_id(entity_id=command.partner_id)

    return list(partner.get_targets_log().values())