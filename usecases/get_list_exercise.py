from interfaces.use_case import GetListExerciseInterface
from interfaces.repository import ExerciseRepositoryInterface
from typing import TextIO, Type


class GetListExercise(GetListExerciseInterface):
    """ This is class get list exercise """

    def __init__(self, repository: Type[ExerciseRepositoryInterface]):
        self.repository = repository

    def file_to_array_transform(self, file: TextIO):
        array = file.file.readlines()
        array = [z.decode("utf-8") for z in array]
        return array
    
    def get_list(self, index_list_exercise: int = None) -> list:
        if index_list_exercise:
            list_exercise = self.repository.get_list(index_list_exercise=int(index_list_exercise))
            result = self.file_to_array_transform(list_exercise[0])
            return [{"text":form, "id":id} for id, form in enumerate(result)]

        list_exercise = self.repository.get_list()

        return [{"list_name":element.list_name, "slug":element.slug.get_slug(), "id":element.id, "availability":True} for element in list_exercise]