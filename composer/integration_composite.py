from controllers import IntegrationController
from usecases import IntegrationMrplato
from mrplatoweb.mrplatoweb.main import ProofWindow,InputArgumentBox
from infra.listexercises import ExerciseRepository

def integration_mrplato_composite():
    pw = ProofWindow()
    inputargument = InputArgumentBox()
    repository = ExerciseRepository()
    usecase = IntegrationMrplato(inputargument=inputargument,proofwindow=pw,repository=repository)
    controller = IntegrationController(usecase=usecase)
    return controller
    