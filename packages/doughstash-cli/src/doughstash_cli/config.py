from dataclasses import dataclass
from pathlib import Path

ENV_DB_PATH = "DOUGHSTASH_DB_PATH"


@dataclass(frozen=True)
class Config:
    db_path: Path
