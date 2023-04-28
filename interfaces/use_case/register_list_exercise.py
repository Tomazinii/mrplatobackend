from abc import ABC, abstractmethod


class RegisterListExerciseInterface(ABC):

    @abstractmethod
    def register(file, list_name):
        raise Exception("method not implemented")
        