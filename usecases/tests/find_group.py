


from unittest.mock import Mock
import pytest
from usecases import FindGroup
from interfaces.repository import GroupRepositoryInterface
from domain.entities.tournamment import Group


pytest.mark.unit

def test_find_group():

    repository = Mock(spec=GroupRepositoryInterface)
    group = Mock(spec=Group)
    repository.find.return_value = group
    usecase = FindGroup(repository)
    result = usecase.find(id=0)

    assert result.name
    assert result.slug