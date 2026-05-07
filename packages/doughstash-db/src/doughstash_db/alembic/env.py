from alembic import context
from doughstash_db.base import Base
from doughstash_db.models import (  # noqa: F401
    account,
    account_type,
    entry,
    institution,
    instrument,
    instrument_type,
)

config = context.config
connection = config.attributes.get("connection")

if connection is None:
    raise RuntimeError(
        "doughstash_db migrations must be run programmatically; "
        "use doughstash_db.migrations.upgrade(engine)."
    )

context.configure(connection=connection, target_metadata=Base.metadata)

with context.begin_transaction():
    context.run_migrations()
