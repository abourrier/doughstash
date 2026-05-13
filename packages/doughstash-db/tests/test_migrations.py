from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from doughstash_db.schema import Base
from doughstash_db.engine import create_engine
from doughstash_db.migrations import upgrade


def test_upgrade_matches_metadata() -> None:
    engine = create_engine("sqlite:///:memory:")
    upgrade(engine)

    with engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        diff = compare_metadata(ctx, Base.metadata)

    assert diff == [], f"migrations diverged from Base.metadata: {diff}"
