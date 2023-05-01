


from abc import ABC, abstractmethod
from domain.entities.tournamment import Group

class FindGroupInterface(ABC):

    @abstractmethod
    def find(id: int) -> Group:
        raise Exception("method not implemented")
    
