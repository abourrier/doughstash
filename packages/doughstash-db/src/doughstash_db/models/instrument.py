from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from doughstash_db.base import Base


class Instrument(Base):
    """A financial instrument that can be held as a position."""

    __tablename__ = "instrument"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    isin: Mapped[str | None] = mapped_column(unique=True)
    instrument_type_id: Mapped[int] = mapped_column(ForeignKey("instrument_type.id"))
