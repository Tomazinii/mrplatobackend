from controllers import IntegrationController
from usecases import IntegrationMrplato, GetListExercise
from mrplatoweb.mrplatoweb.main import ProofWindow,InputArgumentBox
from infra.listexercises.repository import ExerciseRepository


def integration_mrplato_composite():
    pw = ProofWindow()
    inputargument = InputArgumentBox()
    repository = ExerciseRepository()
    usecasesupport = GetListExercise(repository)
    usecase = IntegrationMrplato(inputargument=inputargument,proofwindow=pw,repository=repository, usecasesupport=usecasesupport)
    controller = IntegrationController(usecase=usecase)
    return controller
    