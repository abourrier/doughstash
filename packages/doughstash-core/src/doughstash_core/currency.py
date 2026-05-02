from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Currency:
    """ISO 4217 currency.

    `minor_unit` is the number of decimal digits used for settlement
    amounts (EUR=2, JPY=0, KWD=3). Quoted prices and FX rates may
    carry more precision than this.

    Reference: https://en.wikipedia.org/wiki/ISO_4217
    """

    code: str
    symbol: str
    minor_unit: int


EUR = Currency(code="EUR", symbol="€", minor_unit=2)
