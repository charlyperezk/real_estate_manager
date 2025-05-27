from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import Partner, OperationType, PartnerFee
from ...domain.repositories import PartnerRepository

class SetPartnerFee(Command):
    partner_id: GenericUUID
    operation_type: OperationType
    on_capture: float
    on_close: float

@partner_module.handler(SetPartnerFee)
async def create_partner(command: SetPartnerFee, partner_repository: PartnerRepository, logger: Logger) -> Partner:
    logger.info(f"Setting partner fee to {command.partner_id}")
    
    partner = partner_repository.get_by_id(command.partner_id)

    partner_fee = PartnerFee(
        operation_type=command.operation_type,
        on_capture=command.on_capture,
        on_close=command.on_close
    )
        
    partner.add_fee(partner_fee=partner_fee)
    partner_repository.persist(entity=partner)

    return partner