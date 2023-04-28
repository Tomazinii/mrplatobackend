import pytest
from domain.entities.exercises import Exercises
from faker import Faker
from domain.entities.objectValue import Slug
faker = Faker()

pytestmark = pytest.mark.unit

class TestExercises:

    def test_exercise_entitie(self):
                
        list_name = faker.name()
        slug = Slug.create(list_name)
        with open("lista0.txt","r") as txt:
            array = txt.readlines()

        entitie = Exercises.create(list_name=list_name, file=array)


        assert entitie.list_name == list_name
        assert entitie.slug.get_slug() == slug.get_slug()
        assert entitie.file.get_list() == array