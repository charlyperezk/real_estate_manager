from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Fee, Money
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.entities import Operation, OperationType, AchievementType
from ...domain.repositories import OperationRepository, OperationPartnerRepository
from ...domain.events import PartnerOperationWasCreated

class CreatePartnerOperation(Command):
    property_id: GenericUUID
    strategy_id: GenericUUID
    partner_id: GenericUUID
    achievement_type: AchievementType
    type: OperationType
    fee: Fee
    amount: Money
    description: str

@operation_module.handler(CreatePartnerOperation)
async def create_partner_operation(
        command: CreatePartnerOperation,
        operation_repository: OperationRepository,
        partner_repository: OperationPartnerRepository,
        logger: Logger
    ) -> Operation:
    
    logger.info("Creating partner operation")

    partner = partner_repository.get_by_id(entity_id=command.partner_id)

    operation = Operation(
        id=command.id,
        strategy_id=command.strategy_id,
        property_id=command.property_id,
        partner_id=command.partner_id,
        achievement_type=command.achievement_type,
        type=command.type,
        fee=command.fee,
        amount=command.amount,
        description=command.description,
    )
            
    operation.register_event(        
        PartnerOperationWasCreated(
            achievement_type=operation.achievement_type,
            operation_id=operation.id,
            property_id=operation.property_id,
            partner_id=operation.partner_id,
            type=operation.type,
            status=operation.status,
            created_at=operation.created_at,
            description=operation.description,
            user_id=partner.user_id
        )
    )

    operation_repository.add(entity=operation)
    return operation