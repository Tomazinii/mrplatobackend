

from abc import ABC, abstractmethod


class RegisterMemberInterface(ABC):

    @abstractmethod
    def register(user, group, online, boss = False):
        raise Exception("method not implemented")