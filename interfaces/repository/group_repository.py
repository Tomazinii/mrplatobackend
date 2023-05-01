

from abc import ABC, abstractmethod


class GroupRepositoryInterface(ABC):

    @abstractmethod
    def add(turma, name, slug):
        raise Exception("method not implemented")
    
    @abstractmethod
    def find(id: int):
        raise Exception("method not implemented")
    
