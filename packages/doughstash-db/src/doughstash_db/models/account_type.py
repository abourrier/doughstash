from sqlalchemy.orm import Mapped, mapped_column

from doughstash_db.base import Base


class AccountType(Base):
    """An account category."""

    __tablename__ = "account_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
