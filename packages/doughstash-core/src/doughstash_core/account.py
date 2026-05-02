from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from doughstash_core.currency import Currency


class Account:
    """Base account. Subclasses bind to a specific ISO 4217 currency via `currency`."""

    __slots__ = ()
    currency: ClassVar[Currency]
