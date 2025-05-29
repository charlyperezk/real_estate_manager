from lato import Query
from typing import List
from .. import partner_module
from ...domain.repositories import PartnerRepository, Partner

class GetAllPartners(Query):
    ...

@partner_module.handler(GetAllPartners)
async def get_partner(query: GetAllPartners, partner_repository: PartnerRepository) -> List[Partner]:
    return partner_repository.get_all()