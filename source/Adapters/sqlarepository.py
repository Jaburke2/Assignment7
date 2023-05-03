from sqlalchemy.orm import Session
from Domain.model import Bookmark
from repository import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, bookmark: Bookmark):
        with self.session.begin():
            self.session.add(bookmark)

    def get(self, id: int) -> Bookmark:
        return self.session.query(Bookmark).get(id)

    def get_all(self) -> list[Bookmark]:
        return self.session.query(Bookmark).all()

    def update(self, bookmark: Bookmark):
        with self.session.begin():
            self.session.merge(bookmark)

    def delete(self, id: int):
        bookmark = self.get(id)
        with self.session.begin():
            self.session.delete(bookmark)

