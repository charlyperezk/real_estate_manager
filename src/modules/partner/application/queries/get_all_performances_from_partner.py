from typing import List
from src.seedwork.application.queries import Query
from src.seedwork.domain.value_objects import GenericUUID, Period
from src.seedwork.infrastructure.logging import Logger
from .. import partner_module
from ...domain.entities import PartnerPerformance
from ...domain.repositories import PartnerRepository

class GetAllPartnerPerformance(Query):
    partner_id: GenericUUID
    start: Period=Period(year=2024, month=1)
    end: Period=Period.get_current_period()

@partner_module.handler(GetAllPartnerPerformance)
async def get_all_performances_from_partner(
        query: GetAllPartnerPerformance,
        partner_repository: PartnerRepository,
        logger: Logger
    ) -> List[PartnerPerformance]:
    
    logger.info(f"Retrieving all performances from partner with id {query.partner_id} \
                from: {query.start} to: {query.end}")
    
    partner = partner_repository.get_by_id(entity_id=query.partner_id)    

    return partner.get_performances_by_period_range(start=query.start, end=query.end)