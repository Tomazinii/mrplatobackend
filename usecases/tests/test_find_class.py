



from datetime import date
from unittest.mock import Mock
import pytest

from usecases.find_class import FindClass
from domain.entities.Class import Class
from interfaces.repository import ClassRepository


pytestmark = pytest.mark.unit


class TestFindClass:

    def test_find(self):
        repository = Mock(spec=ClassRepository)
        start = date(2023,4,1)
        obj = Class.create(name="turma", id=1, teacher="asdf", start=start, end=start)
        repository.find.return_value = obj
        usecase = FindClass(repository=repository)
        exec = usecase.find(id=1)
        assert exec.name == "turma"
