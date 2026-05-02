from importlib.resources import files

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import Engine

_ALEMBIC_DIR = str(files("doughstash_db") / "alembic")


def upgrade(engine: Engine, revision: str = "head") -> None:
    """Upgrade the schema at `engine` to `revision` (default `head`)."""
    cfg = Config()
    cfg.set_main_option("script_location", _ALEMBIC_DIR)
    with engine.connect() as connection:
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, revision)
