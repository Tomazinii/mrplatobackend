from interfaces.use_case import GetListExerciseInterface
from interfaces.repository import ExerciseRepositoryInterface
from typing import Type


class GetListExercise(GetListExerciseInterface):
    """ This is class get list exercise """

    def __init__(self, repository: Type[ExerciseRepositoryInterface]):
        self.repository = repository

    def get_list(self, index_list_exercise: int = None) -> list:
        if index_list_exercise:
            index_list_exercise = int(index_list_exercise)
        if index_list_exercise and isinstance(index_list_exercise, int):
            list_exercise = self.repository.get_list(index_list_exercise=index_list_exercise)
            return list_exercise

        list_exercise = self.repository.get_list()
        return list_exercise