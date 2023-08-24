from email import message
from typing import Type
from interfaces.use_case import InsertHypothesisInterface
from mrplatoweb.mrplatoweb.main import ProofWindow,InputAdditionalForm

class InsertHypothesis(InsertHypothesisInterface):
    
    def __init__(self,  proofwindow: Type[ProofWindow], inputadditionalform:Type[InputAdditionalForm]):
        self.proof = proofwindow
        self.inputadditionalform = inputadditionalform


    def insert(self, list_form: list):
        # inForm.input_l = ['∼', ['p', '∧', 'q']] # hypótese inserida pelo usuário

        if not isinstance(list_form,list):
            return {"success":False, "message":"invalid data type", "line": ""}

        pw = self.proof
        pw.resetApp()
        sel_rule = 0 # regra selecionada ADHYP
        pw.selected_rule_index = ('INF', sel_rule)
        pw.infCheckBox = sel_rule
        inForm = self.inputadditionalform
        inForm.input_l = list_form # hypótese inserida pelo usuário

        r, newHypothesys = inForm.inputAditionalFormulaOrHyphotesis(pw)
        message = ""

        if r:
            return {"success":r,"message":"created success","line": str(newHypothesys)}
        elif newHypothesys != str(None):
            return {"success":False, "message":message, "line": str(newHypothesys)}
        else:
            return {"success":False, "message":"Error. Check that the hypotheses are inserted correctly", "line": ""}


