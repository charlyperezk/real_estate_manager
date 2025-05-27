import uuid
from datetime import datetime
from typing import Dict, Union, List

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.schema import Column
from sqlalchemy_json import mutable_json_type
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, DateTime

from ...shared_kernel import AchievementType, OperationStatus, OperationType
from ..domain.entities import (
    Partner,
    PartnershipType,
    PartnershipStatus,
    Partnership,
    PartnerFee,
    PartnerOperation,
    Operations
)
from ..domain.repositories import PartnerRepository

from src.seedwork.infrastructure.data_mapper import DataMapper
from src.seedwork.infrastructure.database import Base
from src.seedwork.infrastructure.repository import SqlAlchemyGenericRepository
from src.seedwork.domain.value_objects import (
    GenericUUID,
    Money,
    Currency,
    Fee,
)

def instantiate_partnership(raw_partnership: List[Dict[str, Union[str, bool]]]) -> Partnership:    
    def cast_partner_fee_from_dict(partner_fee: Dict[str, Union[str, bool]]) -> PartnerFee:                
        return PartnerFee(
            operation_type=OperationType(partner_fee["operation_type"]), # type: ignore
            on_capture=float(partner_fee["on_capture"]), # type: ignore
            on_close=float(partner_fee["on_close"]) # type: ignore
        )
    return Partnership(fees=[cast_partner_fee_from_dict(partner_fee) for partner_fee in raw_partnership])

def instantiate_operations(raw_operations: List[Dict[str, Union[str, bool]]]) -> List[PartnerOperation]:    
    def cast_partner_operation_from_dict(partner_operation: Dict[str, Union[str, bool]]) -> PartnerOperation:                
        return PartnerOperation(
            id=GenericUUID(partner_operation["id"]), # type: ignore
            achievement_type=AchievementType(partner_operation["achievement_type"]), # type: ignore
            created_at=datetime(partner_operation["created_at"]), # type: ignore
            amount=Money(
                amount=float(partner_operation["amount"]["amount"]), # type: ignore
                currency=Currency(partner_operation["amount"]["currency"]) # type: ignore
            ),
            fee=Fee(value=partner_operation["fee"]["value"]), # type: ignore
            status=OperationStatus(partner_operation["status"]), # type: ignore
            strategy_id=GenericUUID(partner_operation["strategy_id"]), # type: ignore
            type=OperationType(partner_operation["type"]) # type: ignore
        )
    
    return [cast_partner_operation_from_dict(op) for op in raw_operations]
    
class PartnerModel(Base):
    __tablename__ = "partners"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(UUIDType(binary=False), index=True, unique=True, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    data = Column(mutable_json_type(dbtype=JSONB, nested=True))

class PartnerDataMapper(DataMapper[Partner, PartnerModel]):
    def model_to_entity(self, instance: PartnerModel) -> Partner:
        d = instance.data
        return Partner(
            id=instance.id,
            name=instance.name, #type: ignore
            type=PartnershipType(instance.type), #type: ignore
            status=PartnershipStatus(instance.status), #type: ignore
            user_id=instance.user_id, #type: ignore
            partnership=instantiate_partnership(d["partnership"]["fees"]), #type: ignore
            operations=Operations(
                operations=instantiate_operations(d['operations']["partner_operations"]), #type: ignore
                registered_operations=int(d['operations']["registered_operations"]) #type: ignore
            ), 
            created_at=instance.created_at #type: ignore  
        )

    def entity_to_model(self, entity: Partner) -> PartnerModel:
        return PartnerModel(
            id=entity.id,
            name=entity.name,
            user_id=entity.user_id,
            type=entity.type,
            status=entity.status,
            created_at=entity.created_at,
            data={
                "partnership": {
                    "fees": entity.get_fees()
                },
                "operations": {
                    "partner_operations": entity.get_operations(),
                    "registered_operations": entity.operations.registered_operations
                }
            }
        )

class PartnerPostgresJsonManagementRepository(PartnerRepository, SqlAlchemyGenericRepository): #type: ignore
    mapper_class = PartnerDataMapper #type: ignore
    model_class = PartnerModel