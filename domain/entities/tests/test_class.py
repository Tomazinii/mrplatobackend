import random
import pytest
from domain.entities.Class import Class
from faker import Faker
from unittest.mock import Mock
from domain.entities.user import User
from datetime import date as dateType
from domain.entities.objectValue import Period

faker = Faker()

pytestmark = pytest.mark.unit

class TestClass:

    def test_create_class(self):
        id = random.randint(0, 500)
        name = faker.name()
        teacher = Mock(spec=User)
        period = Mock(spec=Period)
        date = dateType(2000, 4, 10)
        objeto = Class.create(id=id, name=name, teacher=teacher, date=period)
        period.get_period.return_value = {"start":date, "end": date}
        
        assert objeto.name == name
        assert objeto.teacher == teacher
        assert objeto.id == id
        assert objeto.date.get_period()["start"] == date
        assert objeto.date.get_period()["end"] == date
