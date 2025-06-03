from src.seedwork.application.commands import Command
from src.seedwork.domain.value_objects import GenericUUID, Fee, Period
from src.seedwork.infrastructure.logging import Logger
from .. import operation_module
from ...domain.entities import Operation, AchievementType
from ...domain.repositories import OperationRepository
from ...domain.exceptions import ConsistencyError
from ...domain.service import OperationConsistencyOrchestrator
from ...domain.events import PartnerAchievementOperationRegistered
from .....config.container import PartnerFeesProvider

class RegisterPartnerAchievement(Command):
    strategy_id: GenericUUID
    partner_id: GenericUUID
    achievement_type: AchievementType
    description: str

@operation_module.handler(RegisterPartnerAchievement)
async def register_partner_achievement(
        command: RegisterPartnerAchievement,
        operation_repository: OperationRepository,
        partner_fees_provider: PartnerFeesProvider,
        logger: Logger
    ) -> Operation:
    
    logger.info(f"Registering {command.achievement_type} made for partner {command.partner_id}")

    if not operation_repository.has_real_estate_operation_initialized(strategy_id=command.strategy_id):
        raise ConsistencyError.real_estate_operation_not_found(strategy_id=command.strategy_id)
    
    re_operation = operation_repository.get_real_estate_operation(strategy_id=command.strategy_id)
    tier_fee = partner_fees_provider.get_fee_for(
        partner_id=command.partner_id,
        achievement_type=command.achievement_type,
        operation_type=re_operation.type
    )

    consistency_service = OperationConsistencyOrchestrator(re_operation=re_operation)
    operation = consistency_service.register_achievement(
        achievement_type=command.achievement_type,
        partner_id=command.partner_id,
        description=command.description or f"{command.achievement_type.capitalize()}",
        tier_fee=Fee(value=tier_fee)
    )

    operation.register_event(        
        PartnerAchievementOperationRegistered(
            achievement_type=operation.achievement_type,
            operation_id=operation.id,
            property_id=operation.property_id,
            partner_id=operation.partner_id,
            type=operation.type,
            status=operation.status,
            created_at=operation.created_at,
            description=operation.description,
            revenue=operation.amount,
            period=Period.get_current_period()
        )
    )

    operation_repository.add(entity=operation)
    return operation