from abc import ABC, abstractmethod


class FindUserInterface(ABC):

    @abstractmethod
    def by_id(self, id):
        raise Exception(" Method not implemented")
    
    @abstractmethod
    def by_email(self, email):
        raise Exception(" Method not implemented")