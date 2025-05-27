from lato import Query
from src.seedwork.domain.value_objects import GenericUUID
from .. import partner_module
from ...domain.entities import OperationType, PartnerFee
from ...domain.repositories import PartnerRepository

class GetPartnerFeeByOperationType(Query):
    partner_id: GenericUUID
    operation_type: OperationType

@partner_module.handler(GetPartnerFeeByOperationType)
async def get_partner_fee_by_operation_type(query: GetPartnerFeeByOperationType,
                                             partner_repository: PartnerRepository) -> PartnerFee:
    partner = partner_repository.get_by_id(query.partner_id)
    partner_fee = partner.get_fees(operation_type=query.operation_type)
    assert any(partner_fee), f"Partner doesn't have a fee assigned for {query.operation_type}"
    return next((fee for fee in partner_fee))