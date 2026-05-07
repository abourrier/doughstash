from sqlalchemy.orm import Mapped, mapped_column

from doughstash_db.base import Base


class Institution(Base):
    """A bank, broker, or insurer that holds accounts."""

    __tablename__ = "institution"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
