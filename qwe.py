from mrplatoweb.mrplatoweb.main import ProofWindow, InputArgumentBox
# from usecases.integration_mrplato import IntegrationMrplato

# l = IntegrationMrplato(proofwindow=ProofWindow(), inputargument=InputArgumentBox())

# l.apply([0,1], 2, None,{"type":"INF", "sel_rule":14})





pw = ProofWindow()
# pw.resetApp()
in_box = InputArgumentBox()
sel_rule = 6
sel_lines = [0,1]
list_of_problems = ['1 - p → q , p ⊢ q', '2 - p → q , ~q ⊢ ~p', '3 - p → q , q → s ⊢ p → s', '4 - p , q ⊢ p']

pw.selected_lines = sel_lines
pw.selected_rule_index = ('INF', sel_rule)
pw.infCheckBox = sel_rule

# handle = args[0]
# base = args[1]
# problemListName = args[2]
# line = args[4]

line = list_of_problems[3]

#handle.resetInput()
# self.list_of_problems = self.remove_comments(self.list_of_problems)
pw.n_prove_an_argument(in_box,line)

print('APLYING THE RULE')
r, msg, new_line = pw.appRule()

print(f'r:{r}')

if r:
    print('Processing ended with success!')
    print(f'partial conclusion: {msg}')
else:
    print('PROCESSING ENDED WITH UNSUCESS!')
    print('DIAGNOSYS: ',msg)
