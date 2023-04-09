from abc import ABC, abstractmethod


class GetListExerciseInterface(ABC):
    """ this get list exercise interface """

    @abstractmethod
    def get_list(self, index_list_exercise: int):
        raise Exception("method not implemented")