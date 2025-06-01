from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import Partner
from ...domain.repositories import PartnerRepository
from ...domain.events import PartnerWasActivated

class CreatePartner(Command):
    name: str
    user_id: GenericUUID

@partner_module.handler(CreatePartner)
async def create_partner(command: CreatePartner, partner_repository: PartnerRepository, logger: Logger) -> Partner:
    logger.info("Creating partner")
    
    partner = Partner(
        id=command.id,
        name=command.name,
        user_id=command.user_id,
    )
        
    partner.register_event(
        PartnerWasActivated(
            status=partner.status,
            partner_id=partner.id,
            user_id=partner.user_id,
            name=partner.name,
            tier=partner.tier
        )
    )    

    partner_repository.add(entity=partner)
    return partner