from src.seedwork.application.queries import Query
from src.seedwork.domain.value_objects import GenericUUID, Period
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import PartnerPerformance
from ...domain.repositories import PartnerRepository

class GetPartnerPerformance(Query):
    partner_id: GenericUUID
    period: Period=Period.get_current_period()

@partner_module.handler(GetPartnerPerformance)
async def get_performance(query: GetPartnerPerformance, partner_repository: PartnerRepository,
                          logger: Logger) -> PartnerPerformance:
    logger.info(f"Retrieving performance from partner with id {query.partner_id}")
    partner = partner_repository.get_by_id(entity_id=query.partner_id)    
    
    return partner.get_performance_by_period(period=query.period)