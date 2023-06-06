from typing import Type
from interfaces.use_case import SelectFormInterface, GetListExerciseInterface
from mrplatoweb.mrplatoweb.main import ProofWindow, InputArgumentBox


class SelectForm(SelectFormInterface):
    
    def __init__(self, usecase_getlist: Type[GetListExerciseInterface], service_ProofWindow: ProofWindow, service_InputArgumentBox: InputArgumentBox, service_fms):
        self.usecase = usecase_getlist
        self.service_ProofWindow = service_ProofWindow
        self.service_InputArgumentBox = service_InputArgumentBox
        self.service_fms = service_fms


    def temp_add_new_line(self, list_of_problems:list , new_line: list, index_exercise):

        for element in new_line:
            list_of_problems[index_exercise]["text"] = list_of_problems[index_exercise]["text"].replace("⊢", f", {element} ⊢", 1)
        
        return list_of_problems

    def apply(self, sel_rule: int, sel_lines: int, index_exercise: int, index_list_exercise: int, new_line: list, option_index:int):
        list_of_problems = self.usecase.get_list(index_list_exercise)
        option_id = option_index

        
        if len(new_line) != 0:
            list_of_problems = self.temp_add_new_line(list_of_problems, new_line, index_exercise)

        

        pw = self.service_ProofWindow
        in_box = self.service_InputArgumentBox
        line = list_of_problems[index_exercise]["text"] # problema selecionado
        sel_rule = sel_rule["sel_rule"]  # regra selecionada
        pw.selected_lines = sel_lines 
        pw.selected_rule_index = ('EQ', sel_rule)
        pw.infCheckBox = sel_rule
        pw.n_prove_an_argument(in_box,line)
        ind_form_list = self.service_fms.index_form(0, pw.proof_lines[sel_lines[0]])
        options = pw.get_options(ind_form_list)


        if option_index == "":
            return {"options": options}


        selOption = options[option_index]
        newLine, r, message = pw.getSelectedSubFormula2(selOption, str(pw.proof_lines[sel_lines[0]]))

        if r:
            return {"success":r,"message":message,"line": str(newLine)}
        elif newLine != str(None):
            return {"success":False, "message":message, "line": str(newLine)}
        else:
            return {"success":False, "message":message, "line": ""}
