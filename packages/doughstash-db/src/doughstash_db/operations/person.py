from typing import TYPE_CHECKING

from pyuca import Collator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from doughstash_db.schema import Person

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


_collator = Collator()


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


def _normalize(name: str) -> str:
    stripped = name.strip()
    if not stripped:
        raise ValueError("name must not be empty or whitespace-only")
    if len(stripped) > Person.NAME_MAX_LENGTH:
        raise ValueError(f"name must be at most {Person.NAME_MAX_LENGTH} characters")
    return stripped


def _keyify(name: str) -> bytes:
    """Pack the primary-level UCA weights as bytes.

    Stopping at the first 0 keeps only the base-letter weights, which collapses
    the case, accents, and ligatures (Œ → O+E) — the equivalence we want for
    uniqueness and sort.
    """
    key = _collator.sort_key(name)
    primary = key[: key.index(0)]
    return b"".join(w.to_bytes(4, "big") for w in primary)


def create(session: Session, name: str) -> Person:
    """Insert a person. Raises `NameTaken` if `name` collides under folding."""
    normalized = _normalize(name)
    person = Person(name=normalized, name_key=_keyify(normalized))
    session.add(person)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise NameTakenError(normalized) from e
    return person


def rename(session: Session, person_id: int, new_name: str) -> Person:
    """Update a person's name. Raises `PersonNotFound` or `NameTaken`."""
    person = session.get(Person, person_id)
    if person is None:
        raise PersonNotFoundError(person_id)
    normalized = _normalize(new_name)
    person.name = normalized
    person.name_key = _keyify(normalized)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise NameTakenError(normalized) from e
    return person


def delete(session: Session, person_id: int) -> None:
    """Delete a person. Raises `PersonNotFound` if no such id."""
    person = session.get(Person, person_id)
    if person is None:
        raise PersonNotFoundError(person_id)
    session.delete(person)
    session.commit()


def list_all(session: Session) -> list[Person]:
    """Return all persons sorted by the locale-folded name key."""
    return list(session.scalars(select(Person).order_by(Person.name_key)))
