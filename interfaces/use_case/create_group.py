

from abc import ABC, abstractmethod
from domain.entities.tournamment import Group

class CreateGroupInterface(ABC):

    @abstractmethod
    def create(turma, name) -> Group:
        raise Exception("method not implemented")