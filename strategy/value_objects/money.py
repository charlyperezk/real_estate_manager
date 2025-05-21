from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from .fee import Fee

class Currency(str, Enum):
    USD = "USD"
    ARS = "ARS"

@dataclass(frozen=True, kw_only=True)
class Money:
    amount: float
    currency: Currency = Currency.ARS

    def __repr__(self) -> str:
        return f"Money(amount={round(self.amount, 2)} currency={str(self.currency.value)})"

    def __post_init__(self):
        assert self.amount > 0, "Amount must be greather than 0"

    def __lt__(self, other: Money) -> bool:
        return self.amount < other.amount

    def __gt__(self, other: Money) -> bool:
        return self.amount > other.amount

    def __truediv__(self, other: Money) -> Money:
        return Money(amount=self.amount / other.amount, currency=self.currency)

    def __mul__(self, other: Money) -> Money:
        return Money(amount=self.amount * other.amount, currency=self.currency)

    def __add__(self, other: Money) -> Money:
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: Money) -> Money:
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def calculate_fee_amount(self, fee: Fee) -> Money:        
        amount = (self.amount * fee.value) / 100
        return Money(amount=amount, currency=self.currency)
    
    def calculate_amount_discounting_fee(self, fee: Fee) -> Money:
        return self - self.calculate_fee_amount(fee)
    
