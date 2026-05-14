from typing import TYPE_CHECKING

from doughstash_core.person import NameTakenError, Person, PersonNotFoundError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from doughstash_db.schema import Person as PersonRow

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def create(session: Session, name: str) -> Person:
    """Insert a person. Raises `NameTakenError` if `name` collides under folding."""
    normalized, name_key = Person.normalize(name)
    row = PersonRow(name=normalized, name_key=name_key)
    session.add(row)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise NameTakenError(normalized) from e
    return Person(id=row.id, name=normalized)


def rename(session: Session, person_id: int, new_name: str) -> Person:
    """Update a person's name. Raises `PersonNotFoundError` or `NameTakenError`."""
    row = session.get(PersonRow, person_id)
    if row is None:
        raise PersonNotFoundError(person_id)
    normalized, name_key = Person.normalize(new_name)
    row.name = normalized
    row.name_key = name_key
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise NameTakenError(normalized) from e
    return Person(id=person_id, name=normalized)


def delete(session: Session, person_id: int) -> None:
    """Delete a person. Raises `PersonNotFoundError` if no such id."""
    row = session.get(PersonRow, person_id)
    if row is None:
        raise PersonNotFoundError(person_id)
    session.delete(row)
    session.commit()


def list_all(session: Session) -> list[Person]:
    """Return all persons sorted by the locale-folded name key."""
    rows = session.scalars(select(PersonRow).order_by(PersonRow.name_key))
    return [Person(id=row.id, name=row.name) for row in rows]
