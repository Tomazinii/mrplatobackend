from mrplatoweb.mrplatoweb.main import ProofWindow, InputArgumentBox,fms,InputAdditionalForm
# from usecases.integration_mrplato import IntegrationMrplato

# l = IntegrationMrplato(proofwindow=ProofWindow(), inputargument=InputArgumentBox())

# l.apply([0,1], 2, None,{"type":"INF", "sel_rule":14})

# pw = ProofWindow()
# # pw.resetApp()
# in_box = InputArgumentBox()



pw = ProofWindow()

# PROVANDO INFERÊNCIAS
# print('PROVANDO INFERÊNCIAS')


# list_of_problems = ['25 -   p v q , ∼p , r -> s , q ^ s -> t ^ s ⊢ s ^ t','1 - p → q , p ⊢ q', '2 - p → q , ~q ⊢ ~p', '3 - p → q , q → s ⊢ p → s']
# line = list_of_problems[0] # problema selecionado
# sel_rule = 12 # regra selecionada
# sel_lines = [0,1] # linhas de prova selecionadas


# pw.selected_lines = sel_lines
# pw.selected_rule_index = ('INF', sel_rule)
# pw.infCheckBox = sel_rule

# in_box = InputArgumentBox()

# pw.n_prove_an_argument(in_box,line)
# print('APLYING THE RULE')

# r, msg, new_line= pw.appRule()
# print(f'r:{r}')
# if r:
#     print('Processing ended with success!')
#     print(f'partial conclusion: {msg}')
# else:
#     print('PROCESSING ENDED WITH UNSUCESS!')
#     print('DIAGNOSYS: ',msg)


# print('Selecionando somente uma parte da  linha')

# list_of_problems = ['1 - ~~p ⊢ p -> q', '2 - p → ~~q ⊢ p -> q', '3 - p → ~(p ^ r)  ⊢ p →  (~p v ~r)','4 - ~~p ⊢ p']

# line = list_of_problems[0] # problema selecionado

# sel_rule = 42 # regra selecionada
# sel_lines = [0] # linhas de prova selecionadas

# pw.selected_lines = sel_lines
# pw.selected_rule_index = ('EQ', sel_rule)
# pw.infCheckBox = sel_rule

# pw.n_prove_an_argument(in_box,line)

# ind_form_list = fms.index_form(0, pw.proof_lines[0])
# print(f'ind_form_list: {ind_form_list}')
# options = pw.get_options(ind_form_list)
# print(f'options: {options}')

# selOption = options[0]

# # Chamar  <getSelectedSubFormula2>
# print(f'selOption: {selOption}')
# print(f'proof_lines[0]: {pw.proof_lines[0]}')
# newLine , r, message = pw.getSelectedSubFormula2(selOption, str(pw.proof_lines[0]))
# print(f'Newline: {str(newLine), r}')


#inserindo nova hipótese

sel_rule = 0 # regra selecionada ADHYP

pw.selected_rule_index = ('INF', sel_rule)
pw.infCheckBox = sel_rule

inForm = InputAdditionalForm()
# inForm.input_l = ['∼', ['p', '∧', 'q']] # hypótese inserida pelo usuário
inForm.input_l = [['p', '∧', 'q']] # hypótese inserida pelo usuário

print('APLYING THE RULE')
r, newHypothesys = inForm.inputAditionalFormulaOrHyphotesis(pw)
print(f'NewHYp: {newHypothesys}')

if r:
    print('Processing ended with success!')
else:
    print('PROCESSING ENDED WITH UNSUCESS!')
    print('DIAGNOSYS: ',msg)

#Removendo uma hipótese