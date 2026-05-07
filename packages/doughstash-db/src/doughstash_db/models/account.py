from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from doughstash_db.base import Base


class Account(Base):
    """A financial account held by the user at an institution."""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id"))
    account_type_id: Mapped[int] = mapped_column(ForeignKey("account_type.id"))
