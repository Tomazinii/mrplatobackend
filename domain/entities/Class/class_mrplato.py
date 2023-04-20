from domain.entities.user import User
from datetime import date as dateType

from domain.entities.objectValue import Period

class Class:
    """ entities Class """

    id: int
    name: str
    teacher: User
    date: dateType

    def __init__(self, id: int, name: str, teacher: User, date: dateType):
        self.id = id
        self.name = name
        self.teacher = teacher
        self.date = date

    @staticmethod
    def create(id: int, name: str, teacher: User, date: dateType):
        if isinstance(name, str) and isinstance(id, int) and isinstance(teacher, User) and isinstance(date, Period):
            return Class(id, name, teacher, date)
        
        raise ValueError("invalid type")
