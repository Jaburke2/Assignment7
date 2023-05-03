from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from Domain.model import Bookmark


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, bookmark: Bookmark):
        pass

    @abstractmethod
    def get(self, id: int) -> Bookmark:
        pass

    @abstractmethod
    def get_all(self) -> list[Bookmark]:
        pass

    @abstractmethod
    def update(self, bookmark: Bookmark):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

