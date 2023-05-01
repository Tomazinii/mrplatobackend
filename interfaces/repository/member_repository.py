
from abc import ABC, abstractmethod
from domain.entities.tournamment import Member

class MemberRepositoryInterface(ABC):

    @abstractmethod
    def register(user, group, online, boss) -> Member:
        raise Exception("method not implemented")


    @abstractmethod
    def find_user(user):
        raise Exception("method not implemented")
        