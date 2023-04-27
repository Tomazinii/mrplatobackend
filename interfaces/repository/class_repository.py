from abc import ABC, abstractmethod


class ClassRepository(ABC):

    @abstractmethod
    def create(self, id, name, teacher_id, start, end):
        raise Exception("method no implemented")

    @abstractmethod
    def update(self):
        raise Exception("method no implemented")


    @abstractmethod
    def find(self, id: int):
        raise Exception("method no implemented")

