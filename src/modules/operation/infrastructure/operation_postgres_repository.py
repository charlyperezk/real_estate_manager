import uuid
from sqlalchemy.sql.schema import Column
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, DateTime, Float
from ..domain.entities import Operation, OperationType, AchievementType, OperationStatus
from ..domain.repositories import OperationRepository
from src.seedwork.infrastructure.data_mapper import DataMapper
from src.seedwork.infrastructure.database import Base
from src.seedwork.infrastructure.repository import SqlAlchemyGenericRepository
from src.seedwork.domain.value_objects import (
    Money,
    Currency,
    Fee
)

class OperationModel(Base):
    __tablename__ = "operations"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUIDType(binary=False), index=True, nullable=False)
    strategy_id = Column(UUIDType(binary=False), index=True, nullable=False)
    partner_id = Column(UUIDType(binary=False), index=True, nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    fee = Column(Float, nullable=False)
    achievement_type = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=False)
    in_progress_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=False)

class OperationDataMapper(DataMapper[Operation, OperationModel]):
    def model_to_entity(self, instance: OperationModel) -> Operation:
        return Operation(
            id=instance.id,
            property_id=instance.property_id, #type: ignore
            strategy_id=instance.strategy_id, #type: ignore
            partner_id=instance.partner_id, #type: ignore
            type=OperationType(instance.type),
            amount=Money(amount=instance.price, currency=Currency(instance.currency)),
            fee=Fee(value=instance.fee), #type: ignore
            achievement_type=AchievementType(instance.type), #type: ignore
            description=instance.description, #type: ignore
            status=OperationStatus(instance.status),
            created_at=instance.created_at, #type: ignore
            updated_at=instance.updated_at, #type: ignore
            in_progress_at=instance.in_progress_at, #type: ignore
            completed_at=instance.completed_at, #type: ignore
        )

    def entity_to_model(self, entity: Operation) -> OperationModel:
        return OperationModel(
            id=entity.id,
            property_id=entity.property_id,
            strategy_id=entity.strategy_id,
            partner_id=entity.partner_id,
            fee=entity.fee.value,
            amount=entity.amount.amount,
            currency=entity.amount.currency,
            type=entity.type,
            achievement_type=entity.achievement_type,
            description=entity.description,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            in_progress_at=entity.in_progress_at,
            completed_at=entity.completed_at
        )

class OperationPostgresJsonManagementRepository(OperationRepository, SqlAlchemyGenericRepository): #type: ignore
    mapper_class = OperationDataMapper #type: ignore
    model_class = OperationModel