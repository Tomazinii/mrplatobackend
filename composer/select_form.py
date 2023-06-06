from controllers import SelectFormController
from usecases import SelectForm, GetListExercise
from mrplatoweb.mrplatoweb.main import ProofWindow, InputArgumentBox,fms
from infra.listexercises.repository import ExerciseRepository

def select_form_composite():
    repository = ExerciseRepository()
    usecase_get_list = GetListExercise(repository=repository)
    pw = ProofWindow()
    inputargument = InputArgumentBox()
    usecase = SelectForm(usecase_getlist=usecase_get_list,service_ProofWindow=pw, service_InputArgumentBox=inputargument,service_fms=fms)
    controller = SelectFormController(usecase=usecase)

    return controller