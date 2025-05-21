from src.seedwork.domain.value_objects import GenericUUID
from src.modules.strategy.domain.entities import Fee, Term, Strategy, StrategyStatus, StrategyType, DateRange
from src.modules.strategy.domain.value_objects.money import Currency, Money
from src.modules.strategy.domain.terms_and_conditions import TermType

sell_fee = Fee(value=15)
period = DateRange.from_now_to(weeks=2)
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

if strategy.is_in_renew_alert_period():
    strategy.activate_renew_alert()

print(strategy.collect_events())