from abc import ABC, abstractmethod


class FindUserInterface(ABC):

    @abstractmethod
    def by_id(self):
        raise Exception(" Method not implemented")
    
    @abstractmethod
    def by_email(self):
        raise Exception(" Method not implemented")