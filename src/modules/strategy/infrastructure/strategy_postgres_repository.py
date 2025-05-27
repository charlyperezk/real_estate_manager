import uuid
from typing import Dict, Union, List

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.schema import Column
from sqlalchemy_json import mutable_json_type
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean

from ..domain.entities import Strategy, OperationType, StrategyStatus
from ..domain.terms_and_conditions import TermsAndConditions

from ..domain.value_objects import Term, TermType
from ..domain.repositories import StrategyRepository

from src.seedwork.infrastructure.data_mapper import DataMapper
from src.seedwork.infrastructure.database import Base
from src.seedwork.infrastructure.repository import SqlAlchemyGenericRepository
from src.seedwork.domain.value_objects import (
    Money,
    Currency,
    Fee,
    DateRange,
    RenewAlert
)

"""
References:
"Introduction to SQLAlchemy 2020 (Tutorial)" by: Mike Bayer
https://youtu.be/sO7FFPNvX2s?t=7214
"""

def instantiate_terms(raw_terms: List[Dict[str, Union[str, bool]]]) -> List[Term]:    
    
    def cast_term_from_dict(term: Dict[str, Union[str, bool]]) -> Term:        
        def cast_type(identifier: str) -> Union[TermType, str]:
            return identifier if not identifier in Term.get_default_term_types() else TermType(identifier)
        
        return Term(
            type=cast_type(term['type']), #type: ignore
            active=bool(term['type']),
            description=term['description'] #type: ignore
        )
        
    return [cast_term_from_dict(term) for term in raw_terms]

class StrategyModel(Base):
    __tablename__ = "strategies"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    fee = Column(Float, nullable=False)
    exclusivity = Column(Boolean, nullable=False)
    property_id = Column(UUIDType(binary=False), index=True, nullable=False)
    deposit = Column(Float, nullable=False)
    deposit_currency = Column(String, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime)
    renew_alert = Column(Boolean, nullable=False)
    days_before_renew_alert = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    accepted_by_customer_id = Column(UUIDType(binary=False), nullable=True)
    data = Column(mutable_json_type(dbtype=JSONB, nested=True))

class StrategyDataMapper(DataMapper[Strategy, StrategyModel]):
    def model_to_entity(self, instance: StrategyModel) -> Strategy:
        d = instance.data
        return Strategy(
            id=instance.id,
            type=OperationType(instance.type), #type: ignore
            price=Money(amount=instance.price, currency=Currency(instance.currency)), #type: ignore
            fee=Fee(value=instance.fee), #type: ignore
            exclusivity=instance.exclusivity, #type: ignore
            property_id=instance.property_id, #type: ignore
            deposit=Money(amount=instance.deposit, currency=Currency(instance.deposit_currency)), #type: ignore
            period=DateRange(start=instance.start, end=instance.end), #type: ignore
            renew_alert=RenewAlert(
                active=instance.renew_alert, #type: ignore
                notice_days_threshold=instance.days_before_renew_alert #type: ignore
            ),
            status=StrategyStatus(instance.status), #type: ignore
            accepted_by_customer_id=instance.accepted_by_customer_id, #type: ignore
            terms_conditions=TermsAndConditions( #type: ignore
                terms=instantiate_terms(raw_terms=d["terms_conditions"]["terms"]), #type: ignore 
                registered_terms=int(d["terms_conditions"]["registered_terms"]) #type: ignore
            )
        )

    def entity_to_model(self, entity: Strategy) -> StrategyModel:
        return StrategyModel(
            id=entity.id,
            type=entity.type,
            price=entity.price.amount,
            currency=entity.price.currency,
            fee=entity.fee.value,
            exclusivity=entity.exclusivity,
            property_id=entity.property_id,
            deposit=entity.deposit.amount, # type: ignore
            deposit_currency=entity.deposit.currency, # type: ignore
            start=entity.period.start,
            end=entity.period.end,
            renew_alert=entity.renew_alert.active,
            days_before_renew_alert=entity.renew_alert.notice_days_threshold, # type: ignore
            status=entity.status,
            accepted_by_customer_id=entity.accepted_by_customer_id,
            data={
                "terms_conditions": {
                    "terms": entity.terms_conditions.get_terms(),
                    "registered_terms": entity.terms_conditions.registered_terms
                }
            }
        )

class StrategyPostgresJsonManagementRepository(StrategyRepository, SqlAlchemyGenericRepository): #type: ignore
    mapper_class = StrategyDataMapper #type: ignore
    model_class = StrategyModel