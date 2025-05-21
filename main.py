from src.seedwork.domain.value_objects import GenericUUID
from src.strategy.entities import Fee, Term, Strategy, StrategyStatus, StrategyType, DateRange
from src.strategy.value_objects.money import Currency, Money
from src.strategy.terms_and_conditions import TermType

sell_fee = Fee(value=15)
period = DateRange.from_now_to(weeks=12)
amount = Money(amount=450, currency=Currency.USD)
type = StrategyType.RENT

strategy = Strategy(
    id=GenericUUID.next_id(),
    property_id=GenericUUID.next_id(),
    exclusivity=True,
    fee=sell_fee,
    period=period,
    type=type,
    price=amount,
    deposit=amount
)

strategy.register_term(Term(type=TermType.REGISTERED_WORKER, description="5 AÑOS DE ANTIGUEDAD", active=True))
strategy.register_term(Term(type=TermType.WARRANTY, description="1 garantía propietaria", active=True))
strategy.register_term(Term(type=TermType.PETS, active=False))
strategy.extend_period(weeks=24)
strategy.collect_events()