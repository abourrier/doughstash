from sqlalchemy import Engine, event
from sqlalchemy import create_engine as _sa_create_engine


def create_engine(url: str) -> Engine:
    """Create an SQLAlchemy engine for `url`. Enables foreign-key enforcement on SQLite."""
    engine = _sa_create_engine(url)

    if engine.dialect.name == "sqlite":

        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.close()

    return engine
