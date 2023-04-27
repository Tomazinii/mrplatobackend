


from abc import ABC, abstractmethod


class FindClassInterface(ABC):
    
    @abstractmethod
    def find(id: int):
        raise Exception("method not implemented")