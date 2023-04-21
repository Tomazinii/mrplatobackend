from abc import ABC, abstractmethod
from domain.entities.Class import Class
from typing import Type
from domain.entities.user import User
from domain.entities.objectValue import Period


class CreateClassInterface(ABC):

    @abstractmethod
    def create(id, name, teacher, start, end) -> Type[Class]:
        raise Exception("method not implemented")
    

