from abc import ABC, abstractmethod


class InsertHypothesisInterface(ABC):

    @abstractmethod
    def insert(self, list_form: list):
        raise Exception("method not implemented")