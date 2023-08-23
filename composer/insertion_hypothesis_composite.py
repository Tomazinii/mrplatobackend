
from controllers import InsertionHypothesisController
from mrplatoweb.mrplatoweb.main import InputAdditionalForm,ProofWindow
from usecases import InsertHypothesis

def insert_hypothesis_composite():
    pw = ProofWindow()
    input = InputAdditionalForm()
    usecase = InsertHypothesis(inputadditionalform=input, proofwindow=pw)
    controller = InsertionHypothesisController(usecase=usecase)
    return controller
