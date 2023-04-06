from main import ProofWindow, InputArgumentBox

pw = ProofWindow()
in_box = InputArgumentBox()
sel_rule = 14
sel_lines = [0,1]
list_of_problems = ['1 - p → q , p ⊢ q', '2 - p → q , ~q ⊢ ~p', '3 - p → q , q → s ⊢ p → s']

pw.selected_lines = sel_lines
pw.selected_rule_index = ('INF', sel_rule)
pw.infCheckBox = sel_rule
line = list_of_problems[2]
pw.n_prove_an_argument(in_box,line)

print('APLYING THE RULE')

r, msg = pw.appRule()
print(f'r:{r}')

if r:
    print('Processing ended with success!')
    print(f'partial conclusion: {msg}')
else:
    print('PROCESSING ENDED WITH UNSUCESS!')
    print('DIAGNOSYS: ',msg)

