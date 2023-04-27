
from abc import ABC, abstractmethod


class RegisterUserInterface(ABC):

    @abstractmethod
    def register_users(self, file, Class):
        raise Exception("method not implemented")