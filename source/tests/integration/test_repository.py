import pytest
from datetime import datetime
from source.Adapters.repository import SqlAlchemyRepository
from source.Domain.model import Bookmark
from sqlalchemy import create_engine, select


pytestmark = pytest.mark.usefixtures("mappers")


def test_add_bookmark(sqlite_session_factory):
    repo = SqlAlchemyRepository(sqlite_session_factory())
    b1 = Bookmark(
        title=f"Google.com",
        url=f"http://google.com",
        notes=f"Source of all truth",
        date_added=datetime(2023, 8, 12),
        date_edited=datetime(2023, 8, 12),
    )
    repo.add_one(b1)
    assert repo.get(b1.id) == b1


def test_repository(sqlite_session_factory):
    repo = SqlAlchemyRepository(sqlite_session_factory())

    indexes = ['1', '2', '3']
    bmarks = [Bookmark(
        title=index,
        url=f"http://test{index}.com",
        notes=f"test {index}",
        date_added=datetime(2023, 8, 12),
        date_edited=datetime(2023, 8, 12)
    ) for index in indexes]

    # Test add_one method
    repo.add_one(bmarks[0])
    assert repo.get(bmarks[0].id) == bmarks[0]

    # Test add_many method
    repo.add_many(bmarks[1:])
    queried_bmarks = repo.find_all(select(Bookmark).where(Bookmark.title.in_(indexes)).order_by(Bookmark.title))
    assert len(queried_bmarks) == len(indexes)

    # Test find_first method
    assert repo.find_first(select(Bookmark).where(Bookmark.title == indexes[0])).title == indexes[0]

    # Test update methods
    bmarks[0].notes = 'updated '+bmarks[0].title
    repo.update(bmarks[0])
    updated_bmark = repo.get(bmarks[0].id)
    assert bmarks[0].notes == updated_bmark.notes

    for bookmark in bmarks:
        bookmark.notes = 'updated '+bookmark.title
    repo.update_many(bmarks)
    queried_bmarks = repo.find_all(select(Bookmark).where(Bookmark.title.in_(indexes)).order_by(Bookmark.title))
    for i in range(len(bmarks)):
        assert queried_bmarks[i].notes == bmarks[i].notes

    # Test delete methods
    repo.delete_one(bmarks[0])
    queried_bmarks = repo.find_all(select(Bookmark).where(Bookmark.title.in_(indexes)).order_by(Bookmark.title))
    assert len(bmarks) - 1 == len(queried_bmarks)

    repo.delete_many(queried_bmarks)
    queried_bmarks = repo.find_all(select(Bookmark).where(Bookmark.title.in_(indexes)).order_by(Bookmark.title))
    assert len(queried_bmarks) == 0
