
from controllers import RegisterListExerciseController
from usecases import RegisterListExercise

def register_list_exercise_compisite():
    usecase = RegisterListExercise()
    controller = RegisterListExerciseController(usecase)
    return controller