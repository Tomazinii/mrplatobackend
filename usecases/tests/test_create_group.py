from random import randint
from unittest.mock import Mock
import faker
import pytest
from usecases import CreateGroup
from interfaces.repository import GroupRepositoryInterface
from domain.entities.tournamment import Group
from usecases import FindClass

pytestmark = pytest.mark.unit
faker = faker.Faker()

def test_create_group():
    repository = Mock(spec=GroupRepositoryInterface)
    name = faker.name()
    turma = randint(0,50)
    group = Group.create(name=name, turma=turma)
    repository.add.return_value = group

    usecasesupport = Mock(spec=FindClass)
    usecasesupport.find.return_value = [0]
    usecase = CreateGroup(repository, usecasesupport)
    result = usecase.create(turma=turma, name=name)

    assert result.name == name
    assert result.turma == turma
    assert result.slug.get_slug()
