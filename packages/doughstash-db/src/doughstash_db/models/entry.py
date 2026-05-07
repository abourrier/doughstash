from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from doughstash_db.base import Base


class Entry(Base):
    """An atomic update to an account's pocket."""

    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    kind: Mapped[str]

    __mapper_args__ = {"polymorphic_on": "kind"}  # noqa: RUF012


class CashEntry(Entry):
    """An atomic update to an account's cash pocket."""

    __tablename__ = "cash_entry"

    id: Mapped[int] = mapped_column(ForeignKey("entry.id"), primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 6))

    __mapper_args__ = {"polymorphic_identity": "cash"}  # noqa: RUF012


class PositionEntry(Entry):
    """An atomic update to an account's position pocket."""

    __tablename__ = "position_entry"

    id: Mapped[int] = mapped_column(ForeignKey("entry.id"), primary_key=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instrument.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6))

    __mapper_args__ = {"polymorphic_identity": "position"}  # noqa: RUF012
