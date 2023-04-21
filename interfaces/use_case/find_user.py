from abc import ABC, abstractmethod
from audioop import ratecv


class FindUserInterface(ABC):

    @abstractmethod
    def by_id(self):
        raise Exception(" Method not implemented")
    
    @abstractmethod
    def by_email(self):
        raise Exception(" Method not implemented")