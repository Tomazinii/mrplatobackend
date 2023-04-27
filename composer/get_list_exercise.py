from controllers import GetListExerciseController
from usecases import GetListExercise
from infra.listexercises import ExerciseRepository

def get_list_exercise_composite():
    repository = ExerciseRepository()
    usecase = GetListExercise(repository)
    controller = GetListExerciseController(usecase)
    return controller