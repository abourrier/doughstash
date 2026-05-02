from doughstash_db.engine import create_engine


def test_sqlite_foreign_keys_enabled() -> None:
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        result = conn.exec_driver_sql("PRAGMA foreign_keys").scalar()
    assert result == 1
