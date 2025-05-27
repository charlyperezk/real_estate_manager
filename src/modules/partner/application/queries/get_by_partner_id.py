from lato import Query
from src.seedwork.domain.value_objects import GenericUUID
from .. import partner_module
from ...domain.repositories import PartnerRepository, Partner

class GetPartner(Query):
    partner_id: GenericUUID

@partner_module.handler(GetPartner)
async def get_partner(query: GetPartner, partner_repository: PartnerRepository) -> Partner:
    return partner_repository.get_by_id(query.partner_id)