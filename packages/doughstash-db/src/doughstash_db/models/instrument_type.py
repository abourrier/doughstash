from sqlalchemy.orm import Mapped, mapped_column

from doughstash_db.base import Base


class InstrumentType(Base):
    """An instrument category."""

    __tablename__ = "instrument_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
