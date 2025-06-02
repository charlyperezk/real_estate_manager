from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.repositories import PartnerRepository

class BanPartner(Command):
    partner_id: GenericUUID
    review_operations: bool = True

@partner_module.handler(BanPartner)
async def ban_partner(command: BanPartner, partner_repository: PartnerRepository,
                          logger: Logger) -> None:
    logger.info(f"Baning partner {command.partner_id}")
    partner = partner_repository.get_by_id(entity_id=command.partner_id)
    partner.ban(review_operations=command.review_operations)
    
    partner_repository.persist(entity=partner)