from domain.entities.user import User
from datetime import date as dateType
from domain.entities.objectValue import Period

class Class:
    """ entities Class """

    id: int
    name: str
    teacher: User
    period: Period

    def __init__(self, id: int, name: str, teacher: User, period: Period):
        self.id = id
        self.name = name
        self.teacher = teacher
        self.period = period

    @staticmethod
    def create(id: int, name: str, teacher: User, start: dateType, end: dateType):
        period = Period.create_period(start=start, end=end)
        if isinstance(name, str)  and isinstance(period, Period):
            return Class(id, name, teacher, period)
        raise ValueError("invalid type", name, teacher, period)


