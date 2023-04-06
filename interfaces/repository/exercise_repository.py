from abc import ABC, abstractmethod


class ExerciseRepositoryInterface(ABC):
    """ this is the exercise repository insterface"""

    @abstractmethod
    def get_list(self, index_list_exercise: int):
        raise Exception("Method not implemented")