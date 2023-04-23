import pytest
from domain.entities.objectValue import File

pytestmark = pytest.mark.unit

def test_file():
    with open("user.txt", "r") as txt:
        register_user = txt.readlines()
        file: File = File.create(register_user)

        assert file.get_file() == register_user