
import random
import pytest
from domain.entities.tournamment import Group
from faker import Faker

faker = Faker()

pytestmark = pytest.mark.unit

class TestGroup:

    def test_group(self):
        turma_id = random.randint(0,50)
        name = faker.name()
        entitie = Group.create(turma=turma_id, name=name)

        assert entitie.name == name
        assert entitie.turma == turma_id
        assert entitie.slug.get_slug()
