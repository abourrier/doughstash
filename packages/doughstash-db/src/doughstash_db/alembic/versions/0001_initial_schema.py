"""initial schema

Revision ID: b1d9e7c4a2f8
Revises:
Create Date: 2026-05-07

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "institution",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_institution")),
        sa.UniqueConstraint("name", name=op.f("uq_institution_name")),
    )
    op.create_table(
        "account_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("has_cash_pocket", sa.Boolean(), nullable=False),
        sa.Column("has_positions_pocket", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_account_type")),
        sa.UniqueConstraint("code", name=op.f("uq_account_type_code")),
    )
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("account_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_type_id"],
            ["account_type.id"],
            name=op.f("fk_account_account_type_id_account_type"),
        ),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institution.id"],
            name=op.f("fk_account_institution_id_institution"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_account")),
    )
    op.create_table(
        "instrument_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_instrument_type")),
        sa.UniqueConstraint("code", name=op.f("uq_instrument_type_code")),
    )
    op.create_table(
        "instrument",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("isin", sa.String(), nullable=True),
        sa.Column("instrument_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["instrument_type_id"],
            ["instrument_type.id"],
            name=op.f("fk_instrument_instrument_type_id_instrument_type"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_instrument")),
        sa.UniqueConstraint("isin", name=op.f("uq_instrument_isin")),
    )
    op.create_table(
        "transaction",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transaction")),
    )
    op.create_table(
        "trade",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("direction", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(18, 6), nullable=False),
        sa.Column("fees", sa.Numeric(18, 6), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["transaction.id"],
            name=op.f("fk_trade_id_transaction"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_trade")),
    )
    op.create_table(
        "entry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("transaction_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
            name=op.f("fk_entry_account_id_account"),
        ),
        sa.ForeignKeyConstraint(
            ["transaction_id"],
            ["transaction.id"],
            name=op.f("fk_entry_transaction_id_transaction"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_entry")),
    )
    op.create_table(
        "cash_entry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(18, 6), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["entry.id"],
            name=op.f("fk_cash_entry_id_entry"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cash_entry")),
    )
    op.create_table(
        "position_entry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("instrument_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["entry.id"],
            name=op.f("fk_position_entry_id_entry"),
        ),
        sa.ForeignKeyConstraint(
            ["instrument_id"],
            ["instrument.id"],
            name=op.f("fk_position_entry_instrument_id_instrument"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_position_entry")),
    )


def downgrade() -> None:
    op.drop_table("position_entry")
    op.drop_table("cash_entry")
    op.drop_table("entry")
    op.drop_table("trade")
    op.drop_table("transaction")
    op.drop_table("instrument")
    op.drop_table("instrument_type")
    op.drop_table("account")
    op.drop_table("account_type")
    op.drop_table("institution")
