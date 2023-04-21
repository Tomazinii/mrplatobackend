from abc import ABC, abstractmethod


class ClassRepository(ABC):

    @abstractmethod
    def create(self, id, name, teacher_id, start, end):
        raise Exception("method no implemented")

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def find_class_by_id(self):
        pass
