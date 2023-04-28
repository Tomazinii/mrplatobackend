

from unittest.mock import Mock
import pytest
from interfaces.repository import ExerciseRepositoryInterface
from faker import Faker
from usecases import RegisterListExercise


faker = Faker()

pytestmark = pytest.mark.unit


class TestRegisterExercise:

    def test_register_exercise(self):
        usecase = RegisterListExercise()

        with open("lista0.txt","r") as txt:
            array = txt.readlines()

            list_name = faker.name()
            result = usecase.register(array, list_name)

            assert result["status"] ==  True
            assert result["data"].list_name == list_name
        