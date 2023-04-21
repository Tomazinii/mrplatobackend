from datetime import date
from interfaces.use_case import CreateClassInterface
from interfaces.repository import ClassRepository as ClassRepositoryInterface
from domain.entities.Class import Class
from typing import Type

#provisorio
from unittest.mock import Mock
from domain.entities.user import User


class CreateClass(CreateClassInterface):

    def __init__(self, repository: Type[ClassRepositoryInterface]):
        self.repository = repository

    def create(self, id: int, name: str, teacher: int, start: date, end: date) -> Class:

        """_summary_

        Args:
            id (int): class id
            name (str): class name
            teacher (int): teacher id
            start (date): date start period
            end (date): date finally period

        Returns:
            Class
        """

        user = Mock(spec=User)        

        clas: Class = Class.create(id, name, user, start, end)

        response = self.repository.create(id=clas.id, name=clas.name, teacher_id=clas.teacher.id, start=clas.period.get_period()["start"], end=clas.period.get_period()["end"])

        return response

        
