from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Currency:

    code: str
    symbol: str


EUR = Currency(code="EUR", symbol="€")
