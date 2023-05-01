from unittest.mock import Mock
import pytest
from interfaces.repository import MemberRepositoryInterface
from domain.entities.user import User
from domain.entities.tournamment import Group
from usecases import RegisterMember, FindUser, FindGroup

pytestmark = pytest.mark.unit


class TestMember:

    def test_register(self):
        repository = Mock(spec=MemberRepositoryInterface)
        repository.find_user.return_value = False
        usecase_find_user = Mock(spec=FindUser)
        usecase_find_user.by_id.return_value = [0]
        usecase_find_group = Mock(spec=FindGroup)
        usecase = RegisterMember(repository,usecase_find_group=usecase_find_group, usecase_find_user=usecase_find_user)
        user = Mock(spec=User)
        group = Mock(spec=Group)
        result = usecase.register(True, user, group, False)

        assert result.user.username
        assert result.group.name

