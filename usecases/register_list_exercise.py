from typing import Dict
from interfaces.use_case.register_list_exercise import RegisterListExerciseInterface
from domain.entities.exercises import Exercises

class RegisterListExercise(RegisterListExerciseInterface):

    def register(self, file, list_name) -> Dict[bool, Exercises]:
        list_exercise = Exercises.create(file, list_name)

        if isinstance(list_exercise, Exercises):
            return {'status':True, "data": list_exercise}
        return {'status': False, "data": None}

        