from dataclasses import dataclass, field
from typing import ClassVar

from pyuca import Collator

_collator = Collator()


def _keyify(name: str) -> bytes:
    """Pack the primary-level UCA weights as bytes.

    Stopping at the first 0 keeps only the base-letter weights, which collapses
    the case, accents, and ligatures (Œ → O+E) — the equivalence we want for
    uniqueness and sort.
    """
    key = _collator.sort_key(name)
    primary = key[: key.index(0)]
    return b"".join(w.to_bytes(4, "big") for w in primary)


class NameTakenError(Exception):
    """Raised when a person's name conflicts with an existing entry."""

    def __init__(self, name: str) -> None:
        super().__init__(f"person name already exists: {name!r}")
        self.name = name


class PersonNotFoundError(Exception):
    """Raised when a person id does not exist."""

    def __init__(self, person_id: int) -> None:
        super().__init__(f"no person with id {person_id}")
        self.person_id = person_id


@dataclass(frozen=True, slots=True)
class Person:
    """A person tracked by the app.

    Constructing strips surrounding whitespace from `name`, validates its length,
    and derives `name_key` — the UCA primary-weight fold used for uniqueness
    and sort.
    """

    NAME_MAX_LENGTH: ClassVar[int] = 64

    id: int
    name: str
    name_key: bytes = field(init=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        normalized, key = self.normalize(self.name)
        object.__setattr__(self, "name", normalized)
        object.__setattr__(self, "name_key", key)

    @classmethod
    def normalize(cls, name: str) -> tuple[str, bytes]:
        """Return `(normalized_name, name_key)`. Raises `ValueError` on invalid input."""
        stripped = name.strip()
        if not stripped:
            raise ValueError("name must not be empty or whitespace-only")
        if len(stripped) > cls.NAME_MAX_LENGTH:
            raise ValueError(f"name must be at most {cls.NAME_MAX_LENGTH} characters")
        return stripped, _keyify(stripped)
