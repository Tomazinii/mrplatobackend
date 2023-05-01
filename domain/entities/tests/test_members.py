from unittest.mock import Mock
import pytest
from domain.entities.tournamment import Member
from domain.entities.tournamment import Group
from domain.entities.user import User



pytestmark = pytest.mark.unit


class TestMembers:

    def test_member(self):
        entitie = Member.create(boss=True, user=Mock(spec=User), group=Mock(spec=Group), online=True)
        assert entitie.boss == True
        assert entitie.user
        assert entitie.group
        

