from typing import List, Optional
from .entities import PartnerPerformance
from ...shared_kernel import Period

class PartnerPerformanceOperations:
    @staticmethod    
    def get_performances_inside_period(
        performances: List[PartnerPerformance], 
        start: Optional[Period]=None,
        end: Optional[Period]=None
    ) -> List[PartnerPerformance]:
        if start and end:
            assert start < end, "Start period must be earlier than end"
        
        start = start or Period(year=2020, month=4)
        end = end or Period.get_current_period()
        return [perf for perf in performances if perf.period.inside_range_period(start=start, end=end)]