

import random
from unittest.mock import Mock
import pytest
from domain.entities.user import RegisterUser

pytestmark = pytest.mark.unit



class TestRegisterUser:

    def test_register(self):
        id = random.randint(0,150)
        with open("user.txt") as txt:
            lines = txt.readlines()
        list_user_entitie = RegisterUser.create(lines, Class=id)

        assert list_user_entitie.file == lines
        assert list_user_entitie.Class == id
        assert isinstance(list_user_entitie, RegisterUser)
