from typing import Type,Dict
from mrplatoweb.mrplatoweb.main import ProofWindow, InputArgumentBox
from interfaces.use_case import IntegrationInterface,GetListExerciseInterface
from interfaces.repository import ExerciseRepositoryInterface


class IntegrationMrplato(IntegrationInterface):

    def __init__(self, proofwindow: Type[ProofWindow], inputargument: Type[InputArgumentBox], repository: Type[ExerciseRepositoryInterface],usecasesupport: Type[GetListExerciseInterface]):
        self.proofwindow = proofwindow
        self.inputargument = inputargument
        self.repository = repository
        self.usecase = usecasesupport

    def temp_add_new_line(self, list_of_problems:list , new_line: list, index_exercise):

        for element in new_line:
            list_of_problems[index_exercise]["text"] = list_of_problems[index_exercise]["text"].replace("⊢", f", {element} ⊢", 1)
        
        return list_of_problems
    

    def apply(self, sel_lines: list, index_exercise: int, index_list_exercise: int, selected_rule_index: dict, new_line: list, sub_form_index: list = None) -> dict:
        list_of_problems = self.usecase.get_list(index_list_exercise)


        if len(new_line) != 0:
            list_of_problems = self.temp_add_new_line(list_of_problems, new_line, index_exercise)


        pw = self.proofwindow
        in_box = self.inputargument
        pw.selected_lines = sel_lines
        pw.selected_rule_index = ( selected_rule_index["type"] , selected_rule_index["sel_rule"])
 
        pw.infCheckBox = selected_rule_index["sel_rule"]
        line = list_of_problems[index_exercise]["text"]

        pw.n_prove_an_argument(in_box,line)

        r, msg, new_line = pw.appRule()

    
        new_line = new_line.__str__()

        if r:
            return {"success":r,"message":msg,"line": new_line}
        elif new_line != str(None):
            return {"success":False, "message":msg, "line": new_line}
        else:
            return {"success":False, "message":msg, "line": ""}


