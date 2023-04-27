import random
from unittest.mock import Mock
from faker import Faker
import pytest
from usecases import RegisterUser
from infra.user.repository import UserRepository
from domain.entities.user import User
from interfaces.use_case import FindClassInterface
from interfaces.use_case import FindUserInterface

pytestmark = pytest.mark.unit 

faker = Faker()

class TestRegisterUserTxtUseCase:

    def test_register(self):

        id = random.randint(0,150)
        repository = Mock(spec=UserRepository)

        id_class = random.randint(0,50)
        email = "alecrin@discente.ufg.br"
        
        repository.add.return_value = User.create(id=id, usermame="alecrin", email=email, nick="alecrin", matriculation="4567895465", turma=id)

        find_class_use_case = Mock(spec=FindClassInterface)
        find_user_use_case = Mock(spec=FindUserInterface)
        find_user_use_case.by_email.return_value = False

        usecase: RegisterUser = RegisterUser(repository, find_class_use_case, find_user_use_case)

        with open("user.txt") as txt:
            list_user = txt.readlines()


        result = usecase.register_users(list_user, id_class)
        assert result[0].email.get_email() == email


