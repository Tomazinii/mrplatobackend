
from datetime import date
from unittest.mock import Mock
import pytest
from infra.user.repository import UserRepository

from domain.entities.user import User
from usecases.find_user import FindUser


pytestmark = pytest.mark.unit


class TestFindClass:

    def test_find(self):
        repository = Mock(spec=UserRepository)
        obj = User.create(id=1,usermame="alecrin", email="a@a.com", nick="asdf",matriculation="123456",turma=1)
        repository.find_by_email.return_value = obj
        usecase = FindUser(repository=repository)
        exec = usecase.by_email(email="a@a.com")
        assert exec.username == "alecrin"
