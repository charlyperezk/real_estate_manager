from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import Partner
from ...domain.repositories import PartnerRepository

class DeactivatePartner(Command):
    partner_id: GenericUUID

@partner_module.handler(DeactivatePartner)
async def deactivate_partner(command: DeactivatePartner, partner_repository: PartnerRepository, logger: Logger) -> Partner:
    logger.info(f"Deactivating partner {command.partner_id}")
    partner = partner_repository.get_by_id(entity_id=command.partner_id)
    partner.deactivate()

    partner_repository.persist(partner)
    return partner