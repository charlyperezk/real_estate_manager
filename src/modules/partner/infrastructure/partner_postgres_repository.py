import uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.schema import Column
from sqlalchemy_json import mutable_json_type
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, DateTime
from ...shared_kernel import AchievementType
from ..domain.entities import (
    Partner,
    PartnerTier,
    PartnershipStatus,
    TargetsLog,
    FeePolicy
)
from ..domain.repositories import PartnerRepository
from src.seedwork.infrastructure.data_mapper import DataMapper
from src.seedwork.infrastructure.database import Base
from src.seedwork.infrastructure.repository import SqlAlchemyGenericRepository
    
class PartnerModel(Base):
    __tablename__ = "partners"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), index=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    data = Column(mutable_json_type(dbtype=JSONB, nested=True))

class PartnerDataMapper(DataMapper[Partner, PartnerModel]):
    def model_to_entity(self, instance: PartnerModel) -> Partner:
        d = instance.data
        return Partner(
            id=instance.id,
            name=instance.name, #type: ignore
            user_id=instance.user_id, #type: ignore
            status=PartnershipStatus(instance.status), #type: ignore
            created_at=instance.created_at, #type: ignore  
            targets_log=TargetsLog.from_dict(d["targets_log"]), #type: ignore
            fee_policies={ #type: ignore
                AchievementType(achievement_type): FeePolicy.from_dict(fee_policy)
                for achievement_type, fee_policy in d["fee_policies"].items()
            }
        )

    def entity_to_model(self, entity: Partner) -> PartnerModel:
        return PartnerModel(
            id=entity.id,
            name=entity.name,
            user_id=entity.user_id,
            status=entity.status,
            created_at=entity.created_at,
            data={
                "targets_log": entity.targets_log.as_dict(),
                "fee_policies": {
                    achievement_type: fee_policy.as_dict()
                    for achievement_type, fee_policy in entity.fee_policies.items()
                }
            }
        )

class PartnerPostgresJsonManagementRepository(PartnerRepository, SqlAlchemyGenericRepository): #type: ignore
    mapper_class = PartnerDataMapper #type: ignore
    model_class = PartnerModel