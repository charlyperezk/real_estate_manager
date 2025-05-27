from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import Partner, PartnershipType, Partnership
from ...domain.repositories import PartnerRepository
from ...domain.events import PartnershipWasActivated

class CreatePartner(Command):
    name: str
    user_id: GenericUUID
    type: PartnershipType

@partner_module.handler(CreatePartner)
async def create_partner(command: CreatePartner, partner_repository: PartnerRepository, logger: Logger) -> Partner:
    logger.info("Creating partner")
    
    partner = Partner(
        id=command.id,
        name=command.name,
        user_id=command.user_id,
        type=command.type,
    )
        
    partner.register_event(
        PartnershipWasActivated(
            partner_id=partner.id,
            operations=partner.operations,
            type=partner.type,
            user_id=partner.user_id,
        )
    )    

    partner_repository.add(entity=partner)

    return partner