import uuid
from typing import Dict, Union, List

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.schema import Column
from sqlalchemy_json import mutable_json_type
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean

from ..domain.entities import Strategy, StrategyType, StrategyStatus
from ..domain.terms_and_conditions import Term, TermType, TermsAndConditions
from ..domain.value_objects import (
    Money,
    Currency,
    Fee,
    DateRange
)
from ..domain.repositories import StrategyRepository
from src.seedwork.infrastructure.data_mapper import DataMapper
from src.seedwork.infrastructure.database import Base
from src.seedwork.infrastructure.repository import SqlAlchemyGenericRepository

"""
References:
"Introduction to SQLAlchemy 2020 (Tutorial)" by: Mike Bayer
https://youtu.be/sO7FFPNvX2s?t=7214
"""

def instantiate_terms(raw_terms: List[Dict[str, Union[str, bool]]]) -> List[Term]:
    def is_identifier_in_default_term_types(identifier: str) -> bool:
        return identifier in Term.get_default_term_types()
    
    def instantiate_term(type: str, active: bool, description: str) -> Term:
        return Term(
            type=type,
            active=active,
            description=description
        )

    term_type_field_list = [i['type'] if not is_identifier_in_default_term_types(
        i['type']) else TermType(i['type']) for i in raw_terms] #type: ignore
    active_field_list = [bool(i['active']) for i in raw_terms]
    description_field_list = [i['description'] for i in raw_terms]

    return [instantiate_term(t[0], t[1], t[2]) #type: ignore
            for t in zip(term_type_field_list, active_field_list, description_field_list)] 

class StrategyModel(Base):
    """Data model for listing domain object"""

    __tablename__ = "strategies"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    type = Column(String)
    price = Column(Float)
    currency = Column(String)
    fee = Column(Float)
    exclusivity = Column(Boolean)
    property_id = Column(UUIDType(binary=False), index=True)
    deposit = Column(Float)
    deposit_currency = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    renew_alert = Column(Boolean)
    days_before_renew_alert = Column(Integer)
    status = Column(String)
    accepted_by_customer_id = Column(UUIDType(binary=False), nullable=True)
    data = Column(mutable_json_type(dbtype=JSONB, nested=True))

class StrategyDataMapper(DataMapper[Strategy, StrategyModel]):
    def model_to_entity(self, instance: StrategyModel) -> Strategy:
        d = instance.data
        return Strategy(
            id=instance.id,
            type=StrategyType(instance.type), #type: ignore
            price=Money(amount=instance.price, currency=Currency(instance.currency)), #type: ignore
            fee=Fee(value=instance.fee), #type: ignore
            exclusivity=instance.exclusivity, #type: ignore
            property_id=instance.property_id, #type: ignore
            deposit=Money(amount=instance.deposit, currency=Currency(instance.deposit_currency)), #type: ignore
            period=DateRange(start=instance.start, end=instance.end), #type: ignore
            renew_alert=instance.renew_alert, #type: ignore
            days_before_renew_alert=instance.days_before_renew_alert, #type: ignore
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
            renew_alert=entity.renew_alert,
            days_before_renew_alert=entity.days_before_renew_alert, # type: ignore
            status=entity.status,
            accepted_by_customer_id=entity.accepted_by_customer_id,
            data={
                "terms_conditions": {
                    "terms": entity.terms_conditions.get_terms(),
                    "registered_terms": entity.terms_conditions.registered_terms
                }
            }
        )


class StrategyPostgresJsonManagementRepository(StrategyRepository, SqlAlchemyGenericRepository):
    """Listing repository implementation"""

    mapper_class = StrategyDataMapper
    model_class = StrategyModel