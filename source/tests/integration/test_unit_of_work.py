import unittest
from unittest.mock import MagicMock
from source.services.unit_of_work import SqlAlchemyUnitOfWork
from source.Adapters import repository

class TestSqlAlchemyUnitOfWork(unittest.TestCase):
    def test_enter_creates_session(self):
        session_factory = MagicMock()
        uow = SqlAlchemyUnitOfWork(session_factory)

        with uow:
            session_factory.assert_called_once()

    def test_exit_closes_session(self):
        session = MagicMock()
        session_factory = MagicMock(return_value=session)
        uow = SqlAlchemyUnitOfWork(session_factory)

        with uow:
            pass

        session.close.assert_called_once()

    def test_exit_commits_on_successful_exit(self):
        session = MagicMock()
        session_factory = MagicMock(return_value=session)
        uow = SqlAlchemyUnitOfWork(session_factory)

        with uow:
            pass

        session.commit.assert_called_once()

    def test_exit_rolls_back_on_failed_exit(self):
        session = MagicMock()
        session_factory = MagicMock(return_value=session)
        uow = SqlAlchemyUnitOfWork(session_factory)

        try:
            with uow:
                raise ValueError()
        except ValueError:
            pass

        session.rollback.assert_called_once()

    def test_products_repo(self):
        session = MagicMock()
        session_factory = MagicMock(return_value=session)
        uow = SqlAlchemyUnitOfWork(session_factory)

        with uow:
            repo = uow.bookmarks
            self.assertIsInstance(repo, repository.AbstractRepository)
