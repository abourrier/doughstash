from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from doughstash_db.base import Base


class Transaction(Base):
    """A grouping of entries that together represent a single business event."""

    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str]

    __mapper_args__ = {"polymorphic_on": "kind"}  # noqa: RUF012


class Transfer(Transaction):
    """A movement of cash between two accounts' cash pockets."""

    __mapper_args__ = {"polymorphic_identity": "transfer"}  # noqa: RUF012


class Trade(Transaction):
    """A buy or sell of an instrument within an account.

    `side` is `"buy"` or `"sell"`. A buy has a negative cash entry and a
    positive position entry; a sell has the opposite.
    """

    __tablename__ = "trade"

    id: Mapped[int] = mapped_column(ForeignKey("transaction.id"), primary_key=True)
    side: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    fees: Mapped[Decimal] = mapped_column(Numeric(18, 6))

    __mapper_args__ = {"polymorphic_identity": "trade"}  # noqa: RUF012
