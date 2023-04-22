import random
import pytest
from unittest.mock import Mock
from usecases import CreateClass
from interfaces.repository import ClassRepository
from faker import Faker
from domain.entities.Class import Class
from datetime import date
from domain.entities.user import User

faker = Faker()

pytestmark = pytest.mark.unit


class TestCreateClassUseCase:

    def test_create(self):
        repository = Mock(spec=ClassRepository)
        usecase = CreateClass(repository=repository)
        name = faker.name()
        id = random.randint(0, 500)
        start = date(2023,4,1)
        end = date(2023,4,1)
        teacher = Mock(spec=User)
        # usecase.create(id=id, name=name, teacher=id, start=start, end=end)
        # repository.create.result_value = Class.create(id=id, name=name, teacher=teacher, start=start, end=end)

        assert 1== 1

