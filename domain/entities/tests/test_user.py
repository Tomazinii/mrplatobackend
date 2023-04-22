import random
from unittest.mock import Mock
import pytest
from domain.entities.user import User
from faker import Faker
from domain.entities.Class import Class

faker = Faker()

def test_user_entitie():

    id = random.randint(0,50)
    username = faker.name()
    email = faker.email()
    nick = faker.name()
    matriculation = "78978978978"
    turma = Mock(spec=Class)

    user: User = User.create(turma=turma, email=email, id=id, nick=nick, usermame=username, matriculation=matriculation)

    assert user.email.get_email() == email
    assert user.matriculation == matriculation
    assert user.id == id
    assert user.turma == turma
    assert user.username == username