
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 08:30:41 2021

@author: cedric
"""

# Para encontrar o seu uso da versão kivy,
# print (kivy .__ version__)


from itertools import chain, combinations

import os.path
from pathlib import Path
import zipfile
# from cryptography.fernet import Fernet



from datetime import datetime


import pickle
import copy
import os
from functools import partial
from . import forms as fms
from . import infRules as inf
from . import equivRules as equiv
from . import predRules as pred
from . import deducInfer as ddi


# -----------------------------------------------------------------------------
class InputAdditionalForm():
    '''
        Used to implement the inference rule "addition".
        Provides a simplified version of the input interface.
        It's almost a copy of the class 'InputArgumentBox'
    '''

    input_l = []

    def printMes(self,text):
        if text != 'FUN' and text != 'VAR' and text != 'QNT' and text != 'CST':
            self.input_l.append(text)
        ref = self.ids.in_new_form
        ref.text= ''.join(map(str, self.input_l)) # includes a space between symbols

    def resetMes(self):
        self.ids.sel_buttons.ids.func_spinner_id.text = 'FUN'
        self.ids.sel_buttons.ids.var_spinner_id.text = 'VAR'
        self.ids.sel_buttons.ids.quant_spinner_id.text = 'QNT'
        self.ids.sel_buttons.ids.const_spinner_id.text = 'CST'

    def backMes(self):
        if self.input_l != []:
            self.input_l.pop()
        ref = self.ids.in_new_form
        ref.text= ''.join(map(str, self.input_l))

    def inputAditionalFormulaOrHyphotesis(self, proofWindRef):
        # app = self.parent.parent.parent #mrplato
        app = proofWindRef #mrplatoweb
        # print(f'app: {app}')
        # print(f'self.input_l : {self.input_l}')

        selected_rule = app.selected_rule_index
        ruleType, ruleNumber = selected_rule
        rule_nick = app.rti[ruleNumber].getNick()

        r0, lines = app.get_selected_lines(app) # Checks if the  selected line is forbidden


        # print(f'rule_nick: {rule_nick}')
        # print(f'r0: {r0} - lines: {lines}')

        if rule_nick == 'ADHYP':
            rl = True
            index = len(app.proof_lines)-1
        else:
            rl, index = app.get_just_one_selected_line(lines)

        if r0 and rl:
            prepInpt = PrepareInput()  # Instantiates a new object
            prep_input = prepInpt.removeParenthesis(self.input_l)
            # print(f'prep_input : {prep_input}')
            r, err_message, new_line = fms.generate_represent(prep_input)
            # print(f'r: {r} - msg : {err_message}')
            if r:
                if rule_nick == 'ADD1':  # Rule 'Adição_1: p=> p v q'
                    add_form = fms.Form2(app.proof_lines[index], fms.GlobalConstants.c_or, new_line)
                elif rule_nick == 'ADD2':  # Rule 'Adição_2: p=> q v p'
                    add_form = fms.Form2(new_line, fms.GlobalConstants.c_or, app.proof_lines[index])
                else:  # ADHYP
                    # print('Adding new hyp')
                    app.hypothesis.append(index + 1)  # Includes the new hypothesis in the list o hypothesis
                    add_form = new_line

                app.proof_lines.append(add_form)  # Inclui nova linha na lista de linhas de prova
                print(f'app.proof_lines: {app.proof_lines}')
                app.lineIndex += 1  # incrementa a numeração das linhas de prova
                # app.showNewLine(add_form, str(index), ruleNumber, ruleType)
                print(f'NewLine: {add_form}')

            # app.clearAllCheckBoxes() #kivy
           # self.ids.in_new_form.text = 'Add ADDITIONAL FORMULA' #mrplato
            self.input_l = []
            return r, add_form
        else:
            return r0 and rl, None

# -----------------------------------------------------------------------------
class InputArgumentBox():
    '''
    Implements the input interface.
    The user can input an argument (premisses and a conclusion)
    using menus or reading from a file.
    '''


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p_button_status = False
        self.c_button_status = False
        self.input_premisses = []

    input_l = []

    
    input_conclusion = ''

    # -----------------------------------------------------------------------------
    def resetInput(self):
        '''
        Clear input argument.
        '''

        # print('resetando')
        self.input_l = []
        self.input_premisses = []
        self.input_conclusion = ''

        return

    # -----------------------------------------------------------------------------
    def printMes(self,text):
        '''
        Prints the symbol (~, ^, ... ) selected from menu in input screen.
        :param text: the symbol select by user.
        :return:
        '''
        if text != 'FUN' and text != 'VAR' and text != 'QNT' and text != 'CST':
            self.input_l.append(text)

        # print(f'self.input_l: {self.input_l}')
        self.ids.in_arg.ids.in_prem_or_concl.text= ''.join(map(str, self.input_l)) # includes a space between symbols

        # print(f'self.input_l: {self.ids.in_arg.ids.in_prem_or_concl.text}')

        return

    # -----------------------------------------------------------------------------
    def resetMes(self):
        '''
        Restores the initial label of propositional menu to VAR, after user
        chooses one of the symbols.
        :return:
        '''
        self.ids.sel_buttons.ids.func_spinner_id.text= 'FUN'
        self.ids.sel_buttons.ids.var_spinner_id.text= 'VAR'
        self.ids.sel_buttons.ids.quant_spinner_id.text= 'QNT'
        self.ids.sel_buttons.ids.const_spinner_id.text= 'CST'

    # -----------------------------------------------------------------------------
    def backMes(self):
        '''
        Called when user select the option '<<' from menu, to undo his later choice.
        All actions caused by that choice are undone.
        :return:
        '''
        if self.input_l !=[]:
            self.input_l.pop()
        self.ids.in_arg.ids.in_prem_or_concl.text= ''.join(map(str, self.input_l))

    # -----------------------------------------------------------------------------
    def inputPremiss(self,form):
        '''
        Imput a new premiss.
        The parameter form is just to check if the text ( a string ) in the input screen
        has been changed.
        The input to be processed into a new premiss is stored in the 'self.ids.in_arg_label.text'
        property.
        '''
        # print(f'root.ids: {self.ids}')
        # print(f'root.ids.in_arg.ids: {self.ids.in_arg.   s}')
        # form = self.ids.in_arg.ids.in_prem_or_concl.text

        print('INPUTING PREMISS')
        print(f'form:{form} - type: {type(form)}')
        # if form == 'Input a Premiss or Conclusion': #String de inicialização do campo
        #     # PopupMessage('ENTER A PREMISS FIRST, PLEASE.', '#FF33FF')
        #     return False, 'ENTER A PREMISS FIRST, PLEASE.'
        # if self.input_conclusion != '':  # Conclusion already entered.
        #     PopupMessage('ARGUMENT ALREADY ENTERED.\nGO TO PROOF WINDOW, PLEASE.', '#FF33FF')
        #     return False ,'ARGUMENT ALREADY ENTERED.\nGO TO PROOF WINDOW, PLEASE.'
        # else:
        #    prems = self.ids.in_arg_label.text
        print(f'self.input_l : {self.input_l}')
        prepInpt = PrepareInput()  # instacia um objeto da classe
        prep_input = prepInpt.removeParenthesis(self.input_l)
        print(f'prep_form: {prep_input}')
        self.input_l = []  # reinicia a lista de entrada
        r, err_message, formula = fms.generate_represent(prep_input)
        print(f'r: {r} - formula: {formula}')
        print(f'premiss: {formula} - type: {type(formula)}')
        if r:
            # self.ids.in_arg_label.text = prems + '(P) ' + str(formula) + '\n'
            self.input_premisses.append(formula)
            print(f'input_premisses: {self.input_premisses}')
            # self.ids.in_arg.ids.in_prem_or_concl.text = 'Input a Premiss or Conclusion'
            return True, 'ok'
        else:
            PopupMessage(err_message, '#FF33FF')
            return False, err_message


    # -----------------------------------------------------------------------------
    def inputConclusion(self, ):

        # if self.input_conclusion != '':  # Conclusion already entered.
        #     PopupMessage('ARGUMENT ALREADY ENTERED.\nGO TO PROOF WINDOW, PLEASE.', '#FF33FF')
        #     return False
        # elif self.input_premisses == []:
        #     PopupMessage('****ENTER PREMISSES FIRST, PLEASE.', '#FF33FF')
        #     return False
        # else:
        #     prems = self.ids.in_arg_label.text
            # print(f'conclusion: {self.input_l}')

        if self.input_l == []:  # An empty conclusion
            # PopupMessage('ENTER A CONCLUSION FIRST, PLEASE.', '#FF33FF')
            return False, 'ENTER A CONCLUSION FIRST, PLEASE.'
        else:
            prepInpt = PrepareInput()  # instacia um objeto da classe
            prep_input = prepInpt.removeParenthesis(self.input_l)
            # print(f'prep_conclusion: {prep_input}')
            self.input_l = []  # reinicia a lista de entrada
            r, err_messsage, formula = fms.generate_represent(prep_input)
            if r:
                # self.ids.in_arg_label.text = self.ids.in_arg_label.text\n+'\n'+ str(form)
                # self.ids.in_arg_label.text = self.ids.in_arg_label.text + '\n' + \
                #                              fms.GlobalConstants.c_ass + ' ' + str(formula)
                self.input_conclusion = formula
                # self.ids.in_arg.ids.in_prem_or_concl.text = 'Input a Premiss or Conclusion'
                return True, 'ok'
            else:
                # PopupMessage(err_messsage, '#FF33FF')
                return False, err_messsage


# -----------------------------------------------------------------------------
class PrepareInput():

    def removeParenthesis(self, t_list):
        """
                Remove the caracters '(' e ')', from the input string, as in ['~', 'p', 'v', '(', 'p', '->', 'q', ')']
                producing the lists ['~', 'p', 'v', ['p', '->', 'q']]

            :param t_list: an input character list
            :return: a nes list, without parenthesis
            """
        # print(f't_list: {t_list}')
        # print(f'len(t_list): {len(t_list)}')

        if t_list == []: # An empty list
            return t_list

        elif t_list.count('(') != t_list.count(')'):
            # PopupMessage('DIFFERENT NUMBER OF ( AND ).', '#FF33FF')
            print('DIFFERENT NUMBER OF ( AND ).')
            return([])
        elif (t_list.count('(') == 0) or (t_list.count(')') == 0):
            if len(t_list) > 1:
                return t_list
            else:
                return t_list[0]
        else:
            #Searches for the first occurence of a par (   )
            terms_bet_par, ind_in, ind_f = self.get_terms_between_parenthesis(t_list)
            # Delete the expression between parenthesis in t_list and the quantifier in position ind_in-1
            # print(f'ind_in: {ind_in}')
            # print(f'ind_f: {ind_f}')
            # print(f'terms_bet_par: {terms_bet_par}')
            del (t_list[ind_in:ind_f])
            # print(f't_list: {t_list}')

            if len(terms_bet_par) >= 1:
                t_list.insert(ind_in,terms_bet_par)

            # print(f't_list_final: {t_list} - len: {len(t_list)}')


            if len(t_list) == 1: # t_list contains only one tuple: "( a v b )', for ex.
                return t_list[0]
            else:
                t_list2 = self.removeParenthesis(t_list)
                return t_list2

    # -----------------------------------------------------------------------------
    def get_terms_between_parenthesis(self, t_list):
        """
        sub_list: terms between parenthesis
        t_list: original list withou terms between parenthesis
        ind_in: position of first parenthesis in t_list

        """
        first_occr = t_list.index(')')  # First occurence of ')'
        r_list = t_list[first_occr::-1]
        # Last occurance of '(' before the first ')'
        last_occr = r_list.index('(')
        sub_list = t_list[first_occr - last_occr + 1:first_occr]
        # print(f'sub_list: {sub_list}')
        ind_in = first_occr - last_occr  # Begining of the sub_list
        ind_f = first_occr + 1  # Ending of the sub_list
        # del (t_list[ind_in:ind_f])  # Delete the expression between parenthesis in t_list

        # print(f'rest_t_list: {t_list}')
        return  sub_list, ind_in, ind_f

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# class ProofWindow(GridLayout):
class ProofWindow():
    counter = 0

    basePath = os.path.dirname(os.path.abspath(__file__))

    rti = inf.criateInfRules()
    rte = equiv.criateEquRules()
    rtp = pred.criatePredRules()

    infCkb_ref= {}
    equivCkb_ref= {}
    predCkb_ref= {}
    proofCkb_ref= {}
    selected_lines = []
    selected_rule_index = None
    begin_hypothesis = -1
    forbidden_lines = []
    list_of_problems = []
    # colors =  [(0,0,0,255),(255,0,0,255),(0,0,255,255),(0,0,100,255),(75,0,130,255)]

    # for predicate calculus
    # --------------------------------------------------------
    # previous_used_constant_list = [] # List of vars used in a demonstration
    # bound_variables = [] # List of vars bound to quantifiers
    # previous_free_vars = [] # List of free variables occurring premiss or hypothesis
    # constants_in_free_premisses = []  # List of constants occurring in an open premiss or hypothesis
    # deducted_from_ex_part = []  # List of vars used in existential particularization
    # --------------------------------------------------------

    selected_new_term = None
    selected_quantifier = None
    student = ("00000","cedric")
    file = ("","","")

    # -----------------------------------------------------------------------------
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        # self.initFolders()
        self.resetApp()

        # currentDateTime = datetime.now()
        # year = currentDateTime.date().year
        # month= currentDateTime.date().month
        # limit = 2023 * 12 + 3
        # today = year * 12 + month
        # if today <= limit:
        #     pass
        #   #kivy  self.infCheckBox = self.initInfTable(self.infCkb_ref,self.rti)
        #   #kivt  self.equivCheckBox = self.initEquivTable(self.equivCkb_ref,self.rte)
        #    #kivy self.predCheckBox = self.initPredTable(self.predCkb_ref,self.rtp)
        # else:
        #     print('Sorry! You must update mrPlato to start!')

####kivy
            # App.get_running_app().stop()
        return

# -----------------------------------------------------------------------------
    def initFolders(self):

        if platform == "android": # Check if os is android
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

            self.dir_separator = '/'
            # self.mrplato_base_dir = os.getcwd()+self.dir_separator
            self.mrplato_base_dir =  '/storage/emulated/0/mrplato'

        elif platform == 'win':  # Check if os is windows
            self.dir_separator = '\\'
            self.mrplato_base_dir = os.getcwd()+self.dir_separator
        else:  # os is linux
            self.dir_separator = '/'
            self.mrplato_base_dir = os.getcwd()+self.dir_separator

        self.ARGS_dir =  self.mrplato_base_dir+self.dir_separator+'ARGS'
        self.PROOFS_dir = self.mrplato_base_dir+self.dir_separator+'PROOFS'
        self.LISTS_dir = self.mrplato_base_dir+self.dir_separator+'LISTS'
        self.ZIP_dir = self.mrplato_base_dir+self.dir_separator+'ZIP'

        self.file = ['','','','']

        #
        # print(f'base_dir: {self.mrplato_base_dir}')
        # print(f'ARGS_dir: {self.ARGS_dir}')
        # print(f'PROOFS_dir: {self.PROOFS_dir}')
        # print(f'ZIP_dir: {self.ZIP_dir}')

        if os.path.isdir(self.mrplato_base_dir): # The folder mrplato exists
            print('The base dir <mrplato> already exists in \n'+str(self.mrplato_base_dir))
        else:
            try:
                os.makedirs(self.mrplato_base_dir)  # Create mrplato dir
                print('The base dir <mrplato> was created in \n'+str(self.mrplato_base_dir))
            except:
                print('Unable to create <mrplato> base dir in\n'+str(self.mrplato_base_dir))

                return


        if os.path.isdir(self.ARGS_dir): # Create ARGS dir
            pass
        else:
            try:
                os.makedirs(self.ARGS_dir)
            except:
                err_message = 'Unable to create <ARGS> dir'
                PopupMessage(err_message, '#FF33FF')  # cor lilás

                return


        if os.path.isdir(self.PROOFS_dir):  # Create PROOFS dir
            pass
        else:
            try:
                os.makedirs(self.PROOFS_dir)
            except:
                err_message = 'Unable to create <PROOFS> dir'
                PopupMessage(err_message, '#FF33FF')  # cor lilás

                return

        if os.path.isdir(self.LISTS_dir):  # Create LISTS dir
            pass
        else:
            try:
                os.makedirs(self.LISTS_dir)
            except:
                err_message = 'Unable to create <LISTS> dir'
                PopupMessage(err_message, '#FF33FF')  # cor lilás

                return

        if os.path.isdir(self.ZIP_dir):  # Create ZIP dir
            pass
        else:
            try:
                os.makedirs(self.ZIP_dir)
            except:
                err_message = 'Unable to create <ZIP> dir'
                PopupMessage(err_message, '#FF33FF')  # cor lilás

                return

        return

    # -----------------------------------------------------------------------------
    def resetApp(self):

       #kivy self.time = 0
        self.errors = 0
        self.backs = 0
        self.tProof = 0 # Início do tempo de prova
        self.line_stack = []
        self.lineIndex = 0
        self.premisses = []
        self.conclusion = ''
        self.proof_lines = [] # Proof lines - initially keeps the argument premisses
        self.ex_particularizations = [] # List of proof lines where existential particularization where aplied
        self.selected_rule_index = None
        self.hypothesis = []
        self.forbidden_lines = []
        self.colors = ['#000000','#FF0000','#0000FF','FF00FF','008000'] # Colors for proof lines

        # self.previous_used_constant_list = [] # Constants used em demonstration (by applying particularization)
        # self.bound_variables = []
        # self.previous_free_vars = []
        # self.deducted_from_ex_part = []

#####KIVY
        # ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.status_bar.ids.errors_label
        # ref.text = 'Errors: ' + str(self.errors)
        #
        # ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.status_bar.ids.backs_label
        # ref.text = 'Backs: ' + str(self.backs)
        #
        # ref1 = self.ids.input_or_proof_screen.ids.proof_screen.ids.status_bar.ids.time_label
        # ref1.text 'Backs: ' + str(self.backs)

        errors = 'Errors: ' + str(self.errors)
        backs = 'Backs: ' + str(self.backs)
        times = 'Backs: ' + str(self.backs)


        # ref2 = self.ids.input_or_proof_screen.ids.proof_screen.ids.input_status_bar.ids.file_label
        # ref2.text = "File: Input from screen"
        #
        # inputWindow = self.ids.input_or_proof_screen.ids.input_screen.ids.in_arg_box.ids.in_arg_label
        # inputWindow.text = 'New Argument \n----------------------------\n'
        # proofWindow = self.ids.input_or_proof_screen.ids.proof_screen.ids.p_box.ids.proof_window_box
        # proofWindow.clear_widgets(children=None)

        return

    # -----------------------------------------------------------------------------
    def about(self):
        message = 'Mr. Plato is a didactic tool\n\nto be used in Logic classes\n\n' \
                  'at Informatic Institute (UFG)!\n\n\nAll rights reserved.'
        PopupMessage(message, '#33FF33')
        return

    # -----------------------------------------------------------------------------
    def setUser(self, code):
        # pass
        dic_users = self.loadUsers()

        students = dic_users['users']

        if code in students:
            self.student = (code,students[code])
            message = 'Welcome \n\n'+ students[code]+ '! \n\n \nThanks for using MrPlato!\n\n'
            PopupMessage(message, '#33FF33')
            return
        else:
            print('USER NOT REGISTERED!')
            print('\nSorry, you must be enrolled in Logic to use mrPlato!')
            # MrPlatoApp().close_application()
            App.get_running_app().stop()
            return

    # -----------------------------------------------------------------------------


    # -----------------------------------------------------------------------------


    # -----------------------------------------------------------------------------


    # -----------------------------------------------------------------------------
    def updateClock(self,*args):
        pass
        # ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.status_bar.ids.time_label
        # self.time += 1
        # ref.text = "Time: "+str(self.time)

    # -----------------------------------------------------------------------------
    def getcheckboxes_active(self, *arg):
        '''how to get the active state of all checkboxed created in def show'''
        # Iterate over the dictionary storing the CheckBox widgets
        for idx, wgt in self.proofCkb_ref.items():
            if idx.active :
                self.selected_lines.append(wgt)

        for idx, wgt in self.infCkb_ref.items():
            if idx.ids.rcb.active : # rcb is the index of the CheckBox
                self.selected_rule_index = ('INF',wgt)

        for idx, wgt in self.equivCkb_ref.items():
            if idx.ids.rcb.active :  # rcb is the index of the CheckBox
                self.selected_rule_index = ('EQ',wgt)

        for idx, wgt in self.predCkb_ref.items():
            if idx.ids.rcb.active:  # rcb is the index of the CheckBox
                self.selected_rule_index = ('PRED', wgt)
        return

    # -----------------------------------------------------------------------------
    def clearAllCheckBoxes(self):
        for idx, wgt in self.proofCkb_ref.items():
            idx.active=False
        for idx, wgt in self.infCkb_ref.items():
            idx.ids.rcb.active=False
        for idx, wgt in self.equivCkb_ref.items():
            idx.ids.rcb.active=False
        for idx, wgt in self.predCkb_ref.items():
            idx.ids.rcb.active=False

        self.selected_lines = []
        return

    # -----------------------------------------------------------------------------
    def get_selected_lines(self, ref):
        ''' Checks if the  selected line is forbidden.
            A proof line is forbidden if it is between
             an hypothesis and a consequent, after the
             hypothesis is removed by application
             of the appropriate inference rule.'''

        lines = ref.selected_lines
        for l in lines:
            if l in self.forbidden_lines:
                msg = 'THE LINE < '+ str(l) + ' > WAS SELECTED. '+ \
                  '\nBUT IT IS FORBIDDEN!'
                PopupMessage(msg, '#FF33FF')
                return False, lines

        return True, lines

    # -----------------------------------------------------------------------------
    def get_just_one_selected_line(self,lines):
        if len(lines) == 1:
            return True, lines[0]
        else:
            return False, 0

    # -----------------------------------------------------------------------------
    def openSubFormulaPopup(self):

        print('Obtendo a lista de formulas parciais')

        r0, lines = self.get_selected_lines(self) # Check if the  selected line is forbiden
        print(f'r0: {r0}')
        print(f'lines: {lines}')

        r, index = self.get_just_one_selected_line(lines)
        print(f'r: {r}')
        print(f'index: {index}')
        print(f'self.proof_lines: {self.proof_lines}')


        if r0 and r:
            print(f'index: {index}')
            print(f'form: {self.proof_lines[index]} - {type(self.proof_lines[index])}')
            ind_form_list = fms.index_form(0,self.proof_lines[index])
            print(f'ind_form_list: {ind_form_list}')
            options = self.get_options(ind_form_list)
            print(f'options: {options}')
####################################################
            # pp = PopupGetSubformula2()
            # pp.options = options
            # pp.original_form = str(self.proof_lines[index])
            #
            # #
            # # pp = PopupGetSubformula()
            # # index = lines[0] # Linha selecionada
            # # pp.ids.selText.text = str(self.proof_lines[index])
            # pp.open()
####################################
        else:
            return


        '''how to get the active state of all checkboxed created in def show'''
        # Iterate over the dictionary storing the CheckBox widgets for idx, wgt in self.proofCkb_ref.items():
       # ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.p_box.ids
       #  print(f'ids: {ref}')

    # -----------------------------------------------------------------------------
    def get_options(self, ind_form_list):
        options = []
        for (ind, form ) in ind_form_list:
            options += [str(form) + ' - AT POS '+str(ind)]
        return options

    # -----------------------------------------------------------------------------
    def getSelectedSubFormula2(self,  selection, original_form):
        '''
        Select part of the formula in order to apply a equivalence rule
        '''

        cnt = fms.GlobalConstants
        print(f'selectedLineNumber: {self.selected_lines}')
        print(f' self.selected_rule_index: { self.selected_rule_index}')

        r0 , lines = self.get_selected_lines(self) #Check if the  selected line is forbiden

        print(f'r0: {r0} - lines: {lines}')
        r, selectedLineNumber = self.get_just_one_selected_line(lines)
        print(f'r: {r} - selectedLIneNumber: {selectedLineNumber}')
        if not (r0 and r):
            # PopupMessage(' ERROR IN LINES!!!!!!!!', '#FF33FF')  # cor
            print( 'ERROR IN LINES!!!!!!!!')
            return

        try:
            rule_type, ruleNumber = self.selected_rule_index
        except:
            # PopupMessage('CHOOSE A RULE FIRST.', '#FF33FF')  # cor lilás
            print('CHOOSE A RULE FIRST.')
            return

        print(f'original_form: {original_form} , type :{type(original_form)}')
        print(f'\n\nselection: {selection}, type :{type(selection)}')

        l_selection = selection.split(' - AT POS ')
        print(f'l_selection: {l_selection}')

        sform = l_selection[0]
        sform_o = copy.copy(sform)
        initial_position = l_selection[1]
        print(f'\n\ninitial_position: {initial_position}')
        print(f'sform: {sform} - len(sform): {len(sform)}')
        #
        begin = int(initial_position)
        end = int(initial_position) + len(sform)-1

        print(f'begin: {begin}')
        print(f'end: {end}')

        sform = self.insert_spaces(sform)
        # print(f'sform: {sform}')

        prepInpt = PrepareInput()  # instacia um objeto da classe print(f'l_new_textA: {l_new_text}')
        l_sform = sform.split()  # Transform into a list whithout spaces
        l_sform = list(filter((',').__ne__, l_sform))  # remove all occurences of ',' from the input_string

        print(f'l_sform: {l_sform}')
        prep_input = prepInpt.removeParenthesis(l_sform)
        print(f'prep_input: {prep_input}')
        r, err_message, form = fms.generate_represent(prep_input)
        print(f'form: {form} - type: {type(form)}')
        print(f'r: {r}')

        if r:
            r, msg, new_form = self.appRulePartial(rule_type, ruleNumber, form)
            print(f'newForm0: {new_form} - type: {type(new_form)}')

            s_newForm = str(new_form)

            if len(s_newForm) > 2:
                if original_form[begin-1] == '(' and original_form[end+1] == ')': pass
                else:
                    s_newForm = "("+s_newForm+ ")"

            print(f'newForm: {s_newForm} - type: {type(s_newForm)}')
            s_newForm = s_newForm.replace(cnt.c_not+cnt.c_not,cnt.c_not+' '+cnt.c_not)
            print(f'newForm2: {s_newForm} - type: {type(s_newForm)}')
            print(f'sform_o: {sform_o} - len(sform_o): {len(sform_o)}')
            new_text = original_form.replace(sform_o,s_newForm)
            print(f'new_text: {new_text}')
            prep_new_text = self.prepareNewFormula(new_text)
            print(f'prep_new_text: {prep_new_text}')

            r, err_message, new_line = fms.generate_represent(prep_new_text)
            print(f'new_line: {new_line}')

            if r:
                self.proof_lines.append(new_line)  # Inclui nova linha na lista de linhas de prova
                self.lineIndex += 1  # incrementa a numeração das linhas de prova
                # self.showNewLine(new_line, str(selectedLineNumber), ruleNumber, rule_type)
                newLine = self.generateNewLine(new_line, str(selectedLineNumber), ruleNumber, rule_type)
                return newLine 
            else:
                # PopupMessage(err_message, '#FF33FF')
                print(err_message)
        else:
            # PopupMessage(err_message, '#FF33FF')
            print(err_message)

    # -----------------------------------------------------------------------------
    def appRulePartial(self, rule_type, ruleNumber, formula):

        # print(f'rule_type: {rule_type} - ruleNumber: {ruleNumber} - formula: {formula} - type: {type(formula)}')

        if rule_type == 'EQ':
            rule = self.rte[ruleNumber]
            r, msg, new_line = equiv.applyEquivRule(rule, [formula])
        else:
            rule = self.get_rtp_rule(ruleNumber)
            # rule = self.rtp[index]
            # print(f'rule: {rule}')
            r, msg, new_line =  self.appDMPredRule(formula, rule)
            # print(f'new_line_DM: {new_line}')

        if r:
            return r, ' ', new_line
        else:
            self.errors += 1
            ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.status_bar.ids.errors_label
            ref.text = 'Errors: ' + str(self.errors)
            msg = 'THE RULE <' + rule.name + '>\nCAN NOT BE APPLIED TO THIS FORMULA' + '\n PLEASE, TRY IT AGAIN.'
            PopupMessage(msg, '#FF33FF')  # cor lilás
            r = False

        return r, msg, new_line

    # -----------------------------------------------------------------------------
    def showNewLine(self,newLine,str_lines,ruleNumber,ruleType):

        if ruleType == 'INF':
            rule = self.rti[ruleNumber]
        elif ruleType == 'EQ':
            rule = self.rte[ruleNumber]
        else:
            rule = self.get_rtp_rule(ruleNumber)
            # rule = self.rtp[ruleNumber]
        nick = rule.getNick()

        # Changes line color when an hipothesys is added
        # if nick == 'ADHYP':
        #     self.colors.insert(len(self.colors),self.colors[0])
        #     self.colors = self.colors[1:]
        #
        # line_color = self.colors[0]
        #
        # ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.p_box.ids.proof_window_box
        # proofCheckBox =  ProofCheckBox(size_hint = (0.04,0.15),ident=self.lineIndex,color=(0,0,0,1))
        # ref.add_widget(proofCheckBox)
        #
        # self.proofCkb_ref[proofCheckBox]= self.lineIndex
        # indexLabel = Label(text= str(self.lineIndex),
        #             color=line_color, size_hint=(0.03,0.15))
        # ref.add_widget(indexLabel)
        # ruleNameLabel = Label(text= str(newLine),
        #             color=line_color,  size_hint=(0.25,0.15))
        # ref.add_widget(ruleNameLabel)
        # appliedRuleLabel = Label(text= str_lines+' - '+nick,
        #             color=line_color, size_hint=(.22,.15))
        # ref.add_widget(appliedRuleLabel)
        # self.line_stack.append((proofCheckBox,indexLabel,ruleNameLabel,appliedRuleLabel))
        print('show_new_line')
        print(f'newLine: {newLine} - type {type(newLine)}')
        print(f'self.conclusion: {self.conclusion} - type {type(self.conclusion)}')

        # Changes back line color when an hipothesys is removed
        if (nick == 'ABsd') or (nick == 'RMHYP') :
            self.colors.insert(0,self.colors[-1])
            self.colors = self.colors[:-1]


        if newLine == self.conclusion:
            if len(self.hypothesis) != 0:
                r = False
                message = 'You got to the conclusion, \n\n' \
                          'but do not removed the last Temporary Hypothesis yet.\n\n' \
                          'It must be removed first!'
                # PopupMessage(message, '#FF33FF')
            else:
                r = True
                # self.stopClock()
                # message = 'DEMONSTRATION ENDED \n\nSUCCESSFULLY in '+str(self.time)+ 's .\n\nCONGRATILATIONS !!!'
                message = 'DEMONSTRATION ENDED \n\nSUCCESSFULLY in '+'<<<<<time>>>>>'+ 's .\n\nCONGRATILATIONS !!!'
                # PopupMessage(message,'#33FF33')
                # self.printProofTable()

              #######  Correct here
                # self.saveSolution('FINAL')


                # print('solution saved')
                # self.loadSolution()
        else:
            r = True
            message = ''
        return r, message

    # NEW -----------------------------------------------------------------------------
    def generateNewLine(self, newLine, str_lines, ruleNumber, ruleType):

            if ruleType == 'INF':
                rule = self.rti[ruleNumber]
            elif ruleType == 'EQ':
                rule = self.rte[ruleNumber]
            else:
                rule = self.get_rtp_rule(ruleNumber)
                # rule = self.rtp[ruleNumber]

            if newLine == self.conclusion:
                if len(self.hypothesis) != 0:
                    r = False
                    message = 'You got to the conclusion, \n\n' \
                              'but do not removed the last Temporary Hypothesis yet.\n\n' \
                              'It must be removed first!'
                    # PopupMessage(message, '#FF33FF')
                else:
                    r = True
                    message = 'DEMONSTRATION ENDED \n\nSUCCESSFULLY in ' + '<<<<<time>>>>>' + 's .\n\nCONGRATILATIONS !!!'


            else:
                r = False
                message = ''

            print(f'GenerateNewLine: {message}')

            return newLine, r, message

    # -----------------------------------------------------------------------------
    def save_partial(self):
        self.saveSolution('PARTIAL')

        return

    # -----------------------------------------------------------------------------
    def delLastLine(self):

        if len(self.line_stack) == 0:
            PopupMessage('YOU GOT BACK TO THE INITIAL POINT.','#FF33FF')
            return
        else:
            p = self.line_stack.pop() #remove o último conjundo de widgets (linha) da pilha
            checkBox = p[0]
            line_number = p[1]
            logic_formula = p[2]
            applied_rule = p[3]
            if ('ABsd' in applied_rule.text) or ('RMHYP' in applied_rule.text):
                message = 'REMOVE HYPOTHESYS CAN NOT BE UNDONE.' \
                      '\nRESTART Mr.Plato TO START \n\nTHE PROOF PROCESS AGAIN.'
                PopupMessage(message, '#FF33FF')  # cor lilás
                self.line_stack.append(p)
                return
            else:
                ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.p_box.ids.proof_window_box
                for w in p: # remove the Labels
                    ref.remove_widget(w)
                # If the last line is an hypothesis, it must be removed from the list of hypothesis
                if self.lineIndex in self.hypothesis:
                    self.hypothesis.pop()  # Excludes hypothesis
                if 'PE' in applied_rule.text:
                    self.ex_particularizations.pop()  # remove the last formula from the list of par
                self.lineIndex-=1
                self.proof_lines.pop()  #remove a última linha da lista de linhasticularized formulas
                self.backs += 1

                ref2 = self.ids.input_or_proof_screen.ids.proof_screen.ids.status_bar.ids.backs_label
                ref2.text = 'Backs: ' + str(self.backs)

            return

    # -----------------------------------------------------------------------------
    def check_add_rules(self):
        '''
            Check if the selected rule is <Addition>
        '''

        try:
            self.getcheckboxes_active()
            ruleType, ruleNumber = self.selected_rule_index
        except:
            return False

        # -----------------------------------------------------------Addition rules
        if (ruleType == 'INF'):
            rule = self.rti[ruleNumber]
            rule_nick = rule.getNick()
            # print(f'rule_nick: {rule_nick}')
            add_rules = (rule_nick == 'ADD1') or (rule_nick == 'ADD2') or (rule_nick == 'ADHYP')
            return add_rules
        else:
            return False

    # -----------------------------------------------------------------------------
    #kivy def appRule(self):
    def appRule(self):
        print('START PROVING')
        print(f'self.selected_rule_index: {self.selected_rule_index}')



       #kivy print(f'self.selected_rule_index: {self.selected_rule_index}')

        try:

            ruleType, ruleNumber = self.selected_rule_index


            print(f'ruleType: {ruleType}')
            print(f'ruleNumber: {ruleNumber}')
            if ruleType == 'INF':
                rule = self.rti[ruleNumber] # Selected rule
                rule_nick = rule.getNick()
                print(f'rule_nick: {rule_nick}')

            else:
                rule_nick = 'nothing'
        except:
          #kivy  PopupMessage('CHOOSE A RULE FIRST, PLEASE.', '#FF33FF')  # cor lilás
            return False, 'CHOOSE A RULE FIRST, PLEASE.'
        


        print(f'self.proof_lines:{self.proof_lines}')

        if self.proof_lines == []:
            #kivy PopupMessage('ENTER PREMISSES FIRST, PLEASE.', '#FF33FF')  # cor lilás
            print('No premisses yet')
            return False, 'ENTER PREMISSES FIRST, PLEASE.'
        if rule_nick == 'RMHYP': # Remove hypothesis inference rule

            r, msg, new_line = self.remove_temp_hyphotesis()
            str_lines = str(len(self.proof_lines)-1)

            r1, message = self.update_proof(r, new_line, str_lines)
        elif rule_nick == 'ABsd': # Replace the hypothesis by its negation
            r, msg, new_line = self.remove_temp_hyphotesis_absurd()
            str_lines = str(len(self.proof_lines)-1)

            if r:
  
                r1, message = self.update_proof(r, new_line, str_lines)
        else:

            r1, message, new_line = self.app_Inf_Eq_Pred_rule(ruleType,ruleNumber)

        self.clearAllCheckBoxes()
        return r1, message, new_line

    # -----------------------------------------------------------------------------
    def app_Inf_Eq_Pred_rule(self,ruleType,ruleNumber):

        print('app_Inf_Eq_Pred_rule')

        if self.selected_lines == []:
            #kivy PopupMessage('CHOOSE A PROOF LINE FIRST, PLEASE.', '#FF33FF')  # cor lilás
            return False, 'CHOOSE A PROOF LINE FIRST, PLEASE.'
        else:
            if ruleType == 'INF':  # Inference rule
                r, message, new_line = self.appInfRule(ruleNumber)
            elif ruleType == 'EQ':  # Equivalence rule
                r, message, new_line = self.appEquivRule(ruleNumber)
            else:  # Predicate rule
                r, message = self.appPredRule(ruleNumber)

            return r, message, new_line

    # -----------------------------------------------------------------------------
    def update_proof(self, r,new_line,str_lines):

        ruleType, ruleNumber = self.selected_rule_index
        if r:
            self.lineIndex += 1  # Increments proof line numeration
            r1, message = self.showNewLine(new_line, str_lines, ruleNumber, ruleType)
            # print(f'new_line {new_line} - type: {type(new_line)}')
            self.proof_lines.append(new_line)
        else:
            if ruleType == "INF": rule_name = self.rti[ruleNumber].getName()
            elif ruleType == "EQ": rule_name = self.rte[ruleNumber].getName()
            else:
                rule = self.get_rtp_rule(ruleNumber)
                rule_name = rule.getName()
                # rule_name = self.rtp[ruleNumber].getName()
            self.errors += 1
         #kivy   ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.status_bar.ids.errors_label
            #kivy  ref.text = 'Errors: ' + str(self.errors)
            r1 = False
            message1 = 'THE RULE <' + rule_name + '>\n CAN NOT BE APPIED TO LINES <'
            message = message1 + str_lines + '>. \n PLEASE, TRY IT AGAIN.'
            #kivy PopupMessage(message, '#FF33FF')  # cor lilás
        return r1, message

    # -----------------------------------------------------------------------------
    def prepareNewFormula(self, new_formula):
        # print(f'new_formula: {new_formula}')

        new_formula = self.insert_spaces(new_formula)
        prepInpt = PrepareInput()  # intacia um objeto da classe print(f'l_new_textA: {l_new_text}')
        l_new_formula = new_formula.split() # Transform into a list whithout spaces
        prep_input = prepInpt.removeParenthesis(l_new_formula)
        # print(f'prep_input: {prep_input}')
        return prep_input

    # -----------------------------------------------------------------------------
    def appInfRule(self, ruleNumber):

        print('PROVANDO INFERÊNCIAS')
        proofLines = []
        str_lines = ''
        r, lines = self.get_selected_lines(self) #Check if the  selected line is forbiden
        print(f'r: {r} - lines: {lines}')
        if not r: return 'ok'
        
        rule = self.rti[ruleNumber] # Selected rule
        # rule_nick = rule.getNick()

        # if rule_nick == 'RMHYP':
        #     r, msg, new_line = self.remove_temp_hyphotesis()
        #     str_lines = str(len(self.proof_lines)-1)
        # else:


        for l in lines:
            proofLines.append(self.proof_lines[l])
            str_lines = ','.join(str(l) for l in lines)  # Transforma list de inteiros em string
            print(f'str_lines: {str_lines}')

        print(f'proofLines: {proofLines}')

        new_line = ""

        r, msg, new_line = ddi.applyInferRule(rule, proofLines)  # Aplica a regra selecionada nas
        print(f'new_line: {new_line}')

        if r:
            r1, message = self.update_proof(r, new_line, str_lines)
            return r1, message, new_line
        else:
            return r, msg, new_line

    # -----------------------------------------------------------------------------
    def remove_temp_hyphotesis(self):
        #The last proof line is considered the consequent of the
        #conditional derived from the last introduced hypothesis
        if len(self.hypothesis) != 0:
            begin_hypothesis = self.hypothesis[-1]
            antecedent = self.proof_lines[begin_hypothesis]
            consequent =  self.proof_lines[-1] # Last proof line
            new_line = fms.Form2(antecedent, fms.GlobalConstants.c_if, consequent)
            i = begin_hypothesis
            while i < len(self.proof_lines):
                self.forbidden_lines.append(i)
                i +=1
            # print(f'self.forbidden_lines: {self.forbidden_lines}')
            self.hypothesis.pop() # Excludes hypothesis
            return True, '', new_line
        else:
            message = 'NO HYPOTHESIS WHERE INTRODUCED SO FAR.' \
                      '\nTHE RULE <Remove Hypothesis> CAN NOT BE APPLIED.' \
                      + '\nPLEASE, TRY IT AGAIN.'
            PopupMessage(message, '#FF33FF')  # cor lilás
            return False, '', ''

    # -----------------------------------------------------------------------------
    def remove_temp_hyphotesis_absurd(self):
        # The last proof line is a contradiction
        # so, the negation of the hypothesis can be added to the proof lines
        if len(self.hypothesis) != 0:
            begin_hypothesis = self.hypothesis[-1]
            antecedent = self.proof_lines[begin_hypothesis]
            consequent = self.proof_lines[-1]  # Last proof line
            # print(f' consequent: {consequent} - type: {type(consequent)}')
            # print(f' opnd1: {consequent.getOpnd1()} - type: {type(consequent.getOpnd1())}')
            if consequent.getOpnd1() == fms.GlobalConstants.false:
                new_line = fms.Form1(fms.GlobalConstants.c_not,antecedent)
                # print(f' new_line: {new_line}')
                i = begin_hypothesis
                while i < len(self.proof_lines):
                    self.forbidden_lines.append(i)
                    i += 1
                self.hypothesis.pop()  # Excludes hypothesis
                return True, '', new_line
            else:
                message = 'THIS FORMULA IS NOT A CONTRADICTION.' \
                      '\nTHE RULE <Remove Hypothesis by Absurd> CAN NOT BE APPLIED.' \
                      + '\nPLEASE, TRY IT AGAIN.'
                PopupMessage(message, '#FF33FF')  # cor lilás
                return False, '', ''
        else:
            message = 'NO HYPOTHESIS WHERE INTRODUCED SO FAR.' \
                      '\nTHE RULE <Remove Hypothesis by Absurd> CAN NOT BE APPLIED.' \
                      + '\nPLEASE, TRY IT AGAIN.'
            PopupMessage(message, '#FF33FF')  # cor lilás
            return False, '', ''

    # -----------------------------------------------------------------------------
    def get_rtp_rule(self,rule_number):
        if rule_number <= 3:
            return self.rtp[0][rule_number]
        else:
            return self.rtp[1][rule_number-4]

    # -----------------------------------------------------------------------------
    def appPredRule(self, ruleNumber):
        # print('PROVANDO PREDICADOS')
        # print(f'ruleNumber: {ruleNumber}')
        rule = self.get_rtp_rule(ruleNumber)
        # print(f'rule: {rule}')

        # rule = self.rtp[ruleNumber]  # selected rule
        rule_nick = rule.getNick()
        # print(f'rule_nick: {rule_nick}')

        r0, lines = self.get_selected_lines(self) # Check if the  selected line is forbidden
                                                  # (in case it is between an hypothesis and a conclusiion
                                                  # after the hypothesis is removed )
        r, index = self.get_just_one_selected_line(lines) # Check if the user selected just one line

        if r0 and r:
            rule = self.get_rtp_rule(ruleNumber)
            # rule = self.rtp[ruleNumber]  # Selected rule
            form = self.proof_lines[index]
            # print(f'form: {form} - type: {type(form)}')
            if (rule_nick == 'PU_lr') or (rule_nick == 'PE_lr'):
                if type(form) is not fms.Fof:
                    message = 'THE RULE <' + rule.name + '>\nCAN NOT BE APPLIED TO THIS FORMULA' + '\n PLEASE, TRY IT AGAIN.'
                    # PopupMessage(message, '#FF33FF')  # cor lilás
                    return False, message
                else:
                    self.app_part_rule(form, index, rule_nick)
            elif (rule_nick == 'GU_lr') or (rule_nick == 'GE_lr'):
                self.app_gener_rule(form, index, rule_nick)
            else:
                r, msg, new_line = self.appDMPredRule(form, rule)
                # print(f'update: {new_line} - type: {type(new_line)}')
                if r:
                    r1, message  = self.update_proof(True, new_line, 'x')
                else:
                    # PopupMessage(msg, '#FF33FF')  # cor lilás
                    r1 = False
                    message = msg

        return r1, message


    # -----------------------------------------------------------------------------
    def app_part_rule(self,form,line,rule_nick):

        # print(f'form: {form}')
        # print(f'line: {line}')
        # print(f'rule_nick: {rule_nick}')

        quantifier_list = form.getQuantifiers()
        # print(f'quant_list: {quantifier_list}')
        options = []
        if rule_nick == 'PU_lr':
            for q in quantifier_list: # Get all '∀' quantifiers
                if q.getName() == fms.GlobalConstants.fa: options.append(str(q))
            if options == []:
                error_msg = 'Universal quantifiers not found.' \
                        '\nUniversal particularization \ncan not be applied.'
                PopupMessage(error_msg, '#FF33FF')  # cor lilás
                return
        else:
            for q in quantifier_list: # Get all '∃' quantifiers
                if q.getName() == fms.GlobalConstants.ex: options.append(str(q))
            if options == []:
                error_msg = 'Existential quantifiers not found.' \
                            '\nExistential particularization \nan not be applied.'
                PopupMessage(error_msg, '#FF33FF')  # cor lilás
                return

        if len(options) == 1: # Just one same-type-quantifier in the formula
            self.apply_part_rule_sel_term(line, None, options[0])
        else: # More than one same-type-quantifier in the formula
            popupGetQt = PopupGetOption()
            popupGetQt.options = options
            popupGetQt.title = 'Select one quantifier (including its var), please.'

            popupGetQt.open()
            popupGetQt.bind(title=partial(self.apply_part_rule_sel_term, line))


    # -----------------------------------------------------------------------------
    def apply_part_rule_sel_term(self,*args,**kwargs ):

        # print(f'args: {args} ')
        line = args[0]
        str_sel_quant = args[2]

        # print(f'selected_line_number: {line} ')
        #
        # print(f'self.selected_quantifier: {str_sel_quant} : type: {type(str_sel_quant)}')
        # print(f'l_selection: {str_sel_quant} ')

        sel_quant = fms.Quant(str_sel_quant[:1], str_sel_quant[1])  # ∀x or ∃x

        quant_name = sel_quant.getName()
        quant_var = sel_quant.getVar()
        # print(f'sel_quant: {sel_quant}')
        #
        # print(f'fms.GlobalConstants.list_of_vars: {fms.GlobalConstants.list_of_vars}')

        popupGetQtTerm = PopupGetOption()
        popupGetQtTerm.options = fms.GlobalConstants.list_of_terms
        popupGetQtTerm.title = 'Select a term to replace the variable < '+quant_var+' >, please.'

        popupGetQtTerm.open()
        popupGetQtTerm.bind(title=partial(self.apply_part_rule,line,quant_name,quant_var,sel_quant))
        return


    # -----------------------------------------------------------------------------
    def apply_part_rule(self, *args, **kwargs):

        line = args[0]
        quant_name = args[1]
        quant_var = args[2]
        sel_quant = args[3]
        term_selected = args[5]

        proof_lines_copy = copy.deepcopy(self.proof_lines)
        alowed_lines = self.remove_forbidden_lines(self.forbidden_lines,proof_lines_copy)

        first_order_form = proof_lines_copy[line]

        if quant_name == fms.GlobalConstants.ex:
            if line  not in [p[0] for p in self.ex_particularizations if True]:
                r, msg = ddi.apply_exist_particularization(quant_var, term_selected,
                        first_order_form,alowed_lines)
                if r: self.ex_particularizations.append((line,self.lineIndex + 1, term_selected))
            else:
                r = False
                msg = 'The formula < '+str(self.proof_lines[line])+\
                      ' > has been used before \nin existential particularization.' \
                      '\nThis rule can not be applied \ntwice to the same formula.'
        if quant_name == fms.GlobalConstants.fa:
            r, msg = ddi.apply_universal_particularization( quant_var,term_selected, first_order_form,self.proof_lines)

        if r :
            # print('after -------------------------')
            # print(f'\n\nr: {r}')
            # print(f'msg: {msg}')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # checar se precisa deep copy de novo
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            new_first_order_form = first_order_form
            new_first_order_form.removeQuantifier(sel_quant)  # remove the quantifier from the list of quantifiers

            scope = new_first_order_form.getScope()
            gts = new_first_order_form.getQuantifiers()
            if (gts == []):
                new_first_order_form = scope

            self.selected_lines = []  # reset selected_lines
            self.update_proof(r, new_first_order_form, str(line))
            return
        else:
            PopupMessage(msg, '#FF33FF')  # cor lilás
            return

    #
    # # -----------------------------------------------------------------------------
    # def app_particularization_rule(self):
    #     # print(f'selectedLineNumber: {self.selected_lines}')
    #
    #     self.openSubFormulaPopup()

# -----------------------------------------------------------------------------
    def remove_forbidden_lines(self, forbidden_lines,proof_lines):
        """ Remove forbidden  lines from proof_lines list """
        allowed = []

        i = 0
        while i < len(proof_lines):
            if i in forbidden_lines:
                pass
            else:
                allowed.append(proof_lines[i])
            i += 1
        return allowed
   # -----------------------------------------------------------------------------
    def get_quant_options(self, ind_form_list):
        ''' list_of_ forms: a list o tuples (N, form)
            N is the position of form in the original string.
            Ex: ∀x∃yp(x,y) v ∃zq(z) produces:
                [(0, '∀x∃yp(x,y) v ∃zq(z)'), (0, '∀x∃yp(x,y)'), (13, '∃zq(z)')]
        '''

        options = []
        for (ind, form) in ind_form_list:
            # print(f'ind: {ind}')
            # print(f'form: {form} - type: {type(form)}')
            if type(form) is fms.Fof:
                quantifier_list = form.getQuantifiers()
            else:
                quantifier_list = []

            # print(f'quantifier_list: {quantifier_list}')

            for q in quantifier_list:
                options += [str(q) + ' - AT POS ' + str(ind)]

        # print(f'options: {options}')
        return options

    # -----------------------------------------------------------------------------
    def app_gener_rule(self,form,line,rule_nick):

        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print('APPLYING GENERALIZATION.')

        terms = self.get_scope_terms(form, [])
        options = list(dict.fromkeys(terms))

        # print(f'line: {line}')
        # print(f'forms: {form}')
        # print(f'term-options: {terms}')

        if options == []:
            msg = 'NO TERM TO GENERALIZE! \nPLEASE TRY AGAIN.'
            PopupMessage(msg, '#FF33FF')  # cor lilás
            return
        elif len(options) == 1:
            self.apply_gen_rule_sel_var(line,rule_nick,None,options[0])
        else:
            popupGetVar = PopupGetOption()
            popupGetVar.options =  options
            popupGetVar.title = 'Select one term to generalize, please.'
            popupGetVar.open()
            popupGetVar.bind(title=partial(self.apply_gen_rule_sel_var,line,rule_nick))

    # -----------------------------------------------------------------------------
    def apply_gen_rule_sel_var(self, *args, **kwargs):
        # print(f'args: {args} ')

        line = args[0]
        rule_nick = args[1]
        term_selected = args[3]

        popupGetPd = PopupGetOption()
        popupGetPd.options =  fms.GlobalConstants.list_of_vars
        popupGetPd.title = 'Select a new variable, please.'

        popupGetPd.open()
        popupGetPd.bind(title=partial(self.apply_gen_rule,line,rule_nick,term_selected))

    # -----------------------------------------------------------------------------
    def apply_gen_rule(self, *args, **kwargs):

        # print(f'args: {args} ')

        line = args[0]
        rule_nick = args[1]
        term_selected = args[2]
        new_var = args[4]

        # print(f'new_var: {new_var} ')
        # print(f'term_selected: {term_selected} ')
        # print(f'line: {line}')

        form = self.proof_lines[line]
        # print(f'form: {form}-  type: {type(form)}')

        if type(form) is fms.Fof:
            q_vars = form.getQuantVars()
        else:
            q_vars = []

        if rule_nick == 'GU_lr':
            quant_symbol = fms.GlobalConstants.fa
            prem_and_hyp = self.premisses
            for p in self.hypothesis:
                prem_and_hyp.append(self.proof_lines[p])

            r, msg, new_form  = ddi.apply_univ_gener(form, new_var, term_selected, q_vars,prem_and_hyp,self.ex_particularizations)
            self.continue_to_update(quant_symbol, line, r, msg, new_form,new_var)
            return
        elif rule_nick == 'GE_lr':
            quant_symbol = fms.GlobalConstants.ex

            terms = self.get_scope_terms(form, [])
            form_vars = [x for x in terms if ddi.is_variable(x)]
            # print(f'form_vars: {form_vars}')
            # print(f'term_selected: {term_selected}')
            # print(f'terms: {terms}')
            # print(f'term  occurrence: {terms.count(term_selected)}')

            i = terms.count(term_selected) # Number of occurrences of the constant
            positions = []

            while i > 0:
                positions.append(i)
                i = i-1
            positions.reverse()

            options = self.get_combinations(self.powerset(positions))

            popupGetPd = PopupGetOption()
            popupGetPd.options = options
            popupGetPd.title = 'Select which instance(s) of the constant '+term_selected+' must be replaced.'

            popupGetPd.open()
            popupGetPd.bind(title=partial(self.apply_gen_exist_rule, quant_symbol, line, new_var, q_vars, term_selected, form, form_vars))

            #The selected term is replaced by the new var in formula
            # r,msg, new_form = ddi.apply_exist_gener(new_var, q_vars, term_selected, form, form_vars)
            # self.continue_to_update(quant_symbol, line, r, msg, new_form,new_var)
            # return
        else:
            r = False
            msg = 'Wrong generalization!'
            PopupMessage(msg, '#FF33FF')  # cor lilás
            return

    # -----------------------------------------------------------------------------
    def apply_gen_exist_rule(self, *args, **kwargs):

        # print(f'args: {args} ')

        quant_symbol= args[0]
        line = args[1]
        new_var = args[2]
        q_vars = args[3]
        term_selected = args[4]
        form = args[5]
        form_vars = args[6]
        terms_to_replace = args[8]

        s_index_terms = terms_to_replace.split(' e ')
        index_terms = [int(i) for i in s_index_terms]

        r, msg, new_form = ddi.apply_exist_gener(new_var, q_vars, term_selected, index_terms, form, form_vars)
        self.continue_to_update(quant_symbol, line, r, msg, new_form, new_var)
        return

    # -----------------------------------------------------------------------------
    def continue_to_update(self, quant_symbol, line, r, msg, new_form,new_var):
        if r:
            # print('after -------------------------')
            # print(f'\n\nr: {r}')
            # print(f'msg: {msg}')
            new_quant = fms.Quant(quant_symbol,new_var)

            if type(new_form) is fms.Fof:
                new_form.insertQuantifier(new_quant)
                # print(f'new_quant: {new_quant}')
                new_formula = new_form
            else:
                new_formula = fms.Fof([new_quant],new_form)

            self.selected_lines = []  # reset selected_lines

            self.update_proof(r, new_formula, str(line))
            return
        else:
            PopupMessage(msg, '#FF33FF')  # cor lilás
            return

    # -----------------------------------------------------------------------------
    def powerset(self,list):
        """
        Generates all combinations of the elements. For exemple, if  S = {2, 5, 10}
         it produces {{}, {2}, {5}, {10}, {2, 5}, {2, 10}, {5, 10}, {2, 5, 10}}.
        """
        return chain.from_iterable(combinations(list, r) for r in range(len(list) + 1))

    # -----------------------------------------------------------------------------
    def get_combinations(self, tuples):
        """
                    Generates all combinations of the elements. For exemple, if  S = {2, 5, 10}
                     it produces {{}, {2}, {5}, {10}, {2, 5}, {2, 10}, {5, 10}, {2, 5, 10}}.
        """
        options = []
        for t in tuples:
            if len(t) > 0:
                option = ' e '.join(str(i) for i in t)
                options.append(option)
        return options

    # -----------------------------------------------------------------------------
    def get_scope_terms(self, form, otherVars):
        # print(f'form: {form}: type(form): {type(form)}')
        # print(f'otherVars: {otherVars}')
        if type(form) is fms.Fof:
            vars1 = self.get_scope_terms(form.getScope(), otherVars)
            # print(f'vars1: {vars1}')
            return vars1+otherVars
        elif type(form) is fms.Pred:
            vars =  form.getPredVars()
            return vars+otherVars
        elif type(form) is fms.Form1:
            vars1 = self.get_scope_terms(form.getOpnd1(),otherVars)
            return vars1
        elif type(form) is fms.Form2:
            vars1 = self.get_scope_terms(form.getOpnd1(),otherVars)
            vars2 = self.get_scope_terms(form.getOpnd2(),vars1)
            return vars2
        else:
            return otherVars

    # -----------------------------------------------------------------------------
    def appDM_rl(self, form, rule_name):


        if type(form) is  fms.Fof:
            if type(form.getScope()) is fms.Form1:
                r, msg, new_line = pred.applyPredRule(form)
                return r, msg, new_line
            else:
                msg = 'THE FORMULA IN THE SCOPE OF \nQUANTIFIER(S) DO NOT START WITH "~". \nTHE RULE <' \
                          + rule_name + '>\nCAN NOT BE APPLIED.' + '\n PLEASE, TRY IT AGAIN.'
                # PopupMessage(message, '#FF33FF')  # cor lilás
                return False, msg, None
        elif type(form) is fms.Form1:
            opnd1 = form.getOpnd1()
            r, msg, new_form = self.appDM_rl(opnd1, rule_name)
            if r:
                new_line = fms.Form1(fms.GlobalConstants.c_not, new_form)
                return r, msg, new_line
            else:
                return r, msg, None
        else:
            msg = 'THE FORMULA IS NOT A fof. \nTHE RULE <' \
                      + rule_name + '>\nCAN NOT BE APPLIED.' + '\n PLEASE, TRY IT AGAIN.'
            # PopupMessage(message, '#FF33FF')  # cor lilás
            return False, msg, None

    # -----------------------------------------------------------------------------
    def appDM_lr(self, form, rule_name):

        if type(form) is fms.Form1:
            opnd1 = form.getOpnd1()
            if type(opnd1) is fms.Fof:
                r, msg, new_line = pred.applyNotPredRule(form)
                # print(f'r: {r} new_line: {new_line} ')
                return r, msg, new_line
            elif type(opnd1) is fms.Form1:
                opnd1 = form.getOpnd1()
                r, msg, new_form = self.appDM_lr(opnd1, rule_name)
                # print(f'r: {r} new_form: {new_form} - type: {type(new_form)}')
                if r:
                    new_form1 = fms.Form1(fms.GlobalConstants.c_not, new_form)
                    # print(f'new_form1: {new_form1}')
                    return r, msg, new_form1
                else:
                    return r, msg, None
        else:
            msg = 'THE FORMULA IS NOT A NEGATION OF A Fof. \nTHE RULE <' + rule_name + \
                      '>\nCAN NOT BE APPLIED.' + '\n PLEASE, TRY IT AGAIN.'
            # PopupMessage(msg, '#FF33FF')  # cor lilás
            return False, msg, form

    # -----------------------------------------------------------------------------
    # def appDMPredRule(self,form,line,rule):
    def appDMPredRule(self, form, rule):
        # print(f'form_pred: {form} - type: {type(form)}')

        rule_name = rule.getName()
        rule_nick = rule.getNick()

        # print(f'rule_nick: {rule_nick} ')

        if (rule_nick == 'DME_rl') or (rule_nick == 'DMU_rl'):
            r, msg, new_line = self.appDM_rl(form, rule_name)
        elif (rule_nick == 'DME_lr') or (rule_nick == 'DMU_lr'):
            r, msg, new_line = self.appDM_lr(form, rule_name)
        else:
            msg = 'THE SELECTED RULE CAN NOT BE \nAPPLIED TO PREDICATES. \nTHE RULE <' \
                      + rule_name + '>\nCAN NOT BE APPLIED.' + '\nPLEASE, TRY IT AGAIN.'
            # PopupMessage(msg, '#FF33FF')  # cor lilás
            new_line = ' '
            r = False

        # self.update_proof(True, new_line, str(line))
        return r, msg, new_line

    # -----------------------------------------------------------------------------
    def appEquivRule(self, ruleNumber):
        print('PROVANDO EQUIVALÊNCIAS')

        r0, lines = self.get_selected_lines(self) # Checks if the  selected line is forbidden
        r, index = self.get_just_one_selected_line(lines)

        print(f'lines: {lines}')
        print(f'index: {index}')
        print(f'r: {r}')

        if r0 and r:

            rule = self.rte[ruleNumber]  # Selected rule
            print(f'rule: {rule}')
            print(f'premisses: {self.proof_lines}')
            form = self.proof_lines[index]
            print(f'line: {form} - type: {type(form)}')

            if type(form) is fms.Fof:
                scope = form.getScope()
                quants = form.getQuantifiers()
                r, msg, n_scope = equiv.applyEquivRule(rule, [scope])
                new_line = fms.Fof(quants,n_scope)
            else:
                r, msg, new_line = equiv.applyEquivRule(rule, [form])

            print(f'newLine: {new_line} - type: {type(new_line)}')
            print(f'r: {r} - msg: {msg}')

            if r:
                r1, message = self.update_proof(r, new_line, str(index))
                return  r1, message, new_line
            else:
                return r, msg, new_line
        

    def initInfTable(self,infckb_ref,rti):
        i=0
        ref = self.selRule.ids.i_ruleS.ids.infer_box.ids.infer_screen_box
        # ref = self.selRule.ids.i_ruleS.ids.inf_screen_box
        for r in rti:
            if platform == 'android':
                rule_name = self.rti[r].getNick()
            else:
                rule_name = self.rti[r].getName()

            if i%2 : cl = kivy.utils.get_color_from_hex('#800000')
            else: cl = kivy.utils.get_color_from_hex('#000080')
            btLabel = str('('+str(r)+') ')+ rule_name  + ' : ' + str(self.rti[r])
            # if len(btLabel) > 45 :
            #     f = 2
            # else: f = 1
            infCheckBox = LabelCheckBox(text=btLabel,group='infRule',ident=r,color=cl)
            ref.add_widget(infCheckBox)


            # rCheckBox = RuleCheckBox(size_hint = (0.05,0.15),group='infRule',ident=r,color=cl)
            # ref.add_widget(Label(text= str(i),
            #     color=cl, size_hint=(0.03,0.15)))
            #
            # bt = Button(text=btLabel, size_hint=(0.5, 0.15))
            # bt.on_press = self.setCheck(rCheckBox)
            # ref.add_widget(bt)
            # ref.add_widget(Label(text= str(self.rti[r].getName()),
            #     color=cl, size_hint=(0.23,0.15)))
            # ref.add_widget(Label(text= str(self.rti[r]),
            #     color=cl, size_hint=(0.5,0.15)))
            infckb_ref[infCheckBox]= r
            i+=1
        return infckb_ref

        
    def initEquivTable(self,equivCkb_ref,rte):
        i=0
        ref = self.selRule.ids.e_ruleS.ids.equiv_box.ids.equiv_screen_box

        for r in rte:
            if platform == 'android':
                print('Android')
                rule_name = self.rte[r].getNick()
            else:
                rule_name = self.rte[r].getName()

            if i%2 : cl = kivy.utils.get_color_from_hex('#800000')
            else: cl = kivy.utils.get_color_from_hex('#000080')
            btLabel = str('('+str(r)+') ')+ rule_name + ' : ' + str(self.rte[r])
            equivCheckBox = LabelCheckBox(text=btLabel,group='equivRule',ident=r,color=cl)
            ref.add_widget(equivCheckBox)
            # equivCheckBox = RuleCheckBox(size_hint = (0.06,0.15),group='equivRule',ident=r,color=cl)
            # ref.add_widget(equivCheckBox)
            # ref.add_widget(Label(text= str(i),
            #     color=cl, size_hint=(0.03,0.15)))
            # ref.add_widget(Label(text= str(self.rte[r].getName()),
            #     color=cl, size_hint=(0.23,0.15)))
            # ref.add_widget(Label(text= str(self.rte[r]),
            #     color=cl, size_hint=(0.5,0.15)))
            equivCkb_ref[equivCheckBox]= r
            i+=1
        return equivCkb_ref

    def initPredTable(self,predCkb_ref,rtp):

        ref = self.selRule.ids.p_ruleS.ids.pred_box.ids.pred_screen_box
        for i in [0,1]: # 0 : rtp_inf, 1: rtp_equiv
            rtpi = self.rtp[i]
            if i == 0:
                ref.add_widget(Label(text=str('PREDICATE INFERENCE RULES'),
                             color=(128, 0, 128, 1), size_hint=(0.03, 0.15)))
            else:
                ref.add_widget(Label(text=str('PREDICATE EQUIVALENCE RULES'),
                                 color=(128, 0, 128, 1), size_hint=(0.03, 0.15)))

            for r in rtp[i]:
                if platform == 'android':
                    print('Android')
                    rule_name = rtpi[r].getNick()
                else:
                    rule_name = rtpi[r].getName()

                if i%2 : cl = kivy.utils.get_color_from_hex('#800000')
                else: cl = kivy.utils.get_color_from_hex('#000080')
                btLabel = str('('+str(r+4*i)+') ')+ rule_name + ' : ' + str(rtpi[r])
                predCheckBox = LabelCheckBox(text=btLabel,group='predRule',ident=r,color=cl)
                ref.add_widget(predCheckBox)

                predCkb_ref[predCheckBox]= r+4*i

        return predCkb_ref
    
    def initProof(self,premisses,conclusion):

        print('INIT PROOF')

        self.proof_lines = premisses
        self.premisses = premisses.copy() # Just a copy of input premisses
        self.conclusion = conclusion
        #kivy
        # ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.p_box.ids.proof_window_box
        # con_label_ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.conclusion_bar.ids.concl_label
        # con_label_ref.text = fms.GlobalConstants.c_ass+' '+ str(conclusion)

        # label = fms.GlobalConstants.c_ass+' '+ str(conclusion)
        # print(f'LABEL: {label}')

        print(f'self.premisses: {self.premisses}')
        i = 0
        lines = []
        while i < len(premisses):
            print(i)
            print(f'premisses[{i}] : {premisses[i]}')
            lines.append(str(premisses[i])+' P')
            print(f'lines[{i}] : {lines[i]}')
            #kivy
            # proofCheckBox = ProofCheckBox(size_hint=(0.04, 0.15), ident=i, color=(0, 0, 0, 1))
            # ref.add_widget(proofCheckBox)
            # ref.add_widget(Label(text=str(i),
            #                      color=(0, 0, 0, 1), size_hint=(0.03, 0.15)))
            # ref.add_widget(Label(text=str(premisses[i]),
            #  color=(0, 0, 0, 1), size_hint=(0.25, 0.15)))
            # self.proofCkb_ref[proofCheckBox] = i
            # ref.add_widget(Label(text='P',
            #                      color=(0, 0, 0, 1), size_hint=(.22, .15)))
            i += 1
        # if i > 0:
        #     lines[i] = '--'

            #kivy
            # ref.add_widget(Label(text='--',
            #                      color=(0, 0, 0, 1), size_hint=(.04, .15)))
            # ref.add_widget(Label(text='--',
            #                      color=(0, 0, 0, 1), size_hint=(.03, .15)))
            # ref.add_widget(Label(text='-----------------------------------',
            #                      color=(0, 0, 0, 1), size_hint=(.25, .15)))
            # ref.add_widget(Label(text='----------------',
            #                      color=(0, 0, 0, 1), size_hint=(.22, .15)))

            # self.lineIndex = len(premisses) - 1  # Atualiza a numeração das linhas de prova

        # self.startClock()
        print(f'lines: ',lines)
        return
# -----------------------------------------------------------------------------
#     def check_for_free_variables(self, premisses):
#
#         for p in premisses:
#             # print(f'premiss: {p} - type: {type(p)}')
#             free_vars = self.get_free_variables_in_form([],p)
#             # print(f'free_vars: {free_vars}')
#             self.previous_free_vars = free_vars

        # print(f'self.previous_free_vars: {self.previous_free_vars}')
        # print(f'self.deducted_from_ex_part: {self.deducted_from_ex_part}')

# -----------------------------------------------------------------------------
#     def get_free_variables_in_form(self, var_list, premiss):
#
#         # print(f'var_list: {var_list}')
#
#         if type(premiss) is fms.Fof:
#             l_var_quants = premiss.getQuantVars()
#             # l_quants = premiss.getQuantifiers()
#             # l_var_quants = []
#             # for q in l_quants: # Gets variable names of all quantifiers
#             #     varq = q.getVar()
#             #     l_var_quants.append(varq)
#             # print(f'l_var_quants: {l_var_quants}')
#
#             terms = self.get_scope_terms(premiss, [])
#             terms = list(dict.fromkeys(terms))
#             # print(f'terms: {terms}')
#
#             for t in terms:
#                 if t in fms.GlobalConstants.list_of_vars:
#                     if t not in l_var_quants:
#                         var_list.append(t)
#                         # self.previous_free_vars.append(t)
#
#             return var_list
#
#         elif type(premiss) is fms.Pred:
#             terms = self.get_scope_terms(premiss, [])
#             terms = list(dict.fromkeys(terms))
#             # print(f'terms: {terms}')
#             for t in terms:
#                 if t in fms.GlobalConstants.list_of_vars:
#                     var_list.append(t)
#                     # self.previous_free_vars.append(t)
#             return var_list
#         elif type(premiss) is fms.Form1:
#             self.get_free_variables_in_form(var_list,premiss.getOpnd1())
#             return var_list
#         elif type(premiss) is fms.Form2:
#             self.get_free_variables_in_form(var_list,premiss.getOpnd1())
#             self.get_free_variables_in_form(var_list,premiss.getOpnd2())
#             return var_list
#         else:
#             return var_list

    # -----------------------------------------------------------------------------
    def zipDir(self):

        zipFolder = '/ZIP'
        now = datetime.now()
        now_string = now.strftime("%d_%m_%Y-%H_%M")

        if self.file[3] == '':
            proofFolder = self.PROOFS_dir  # Solution folder
            zip_file_name =  str(self.student[0]) + "_" +'proofs'+ "_" + str(now_string) +'.zip' # .zip file name
        else:
            proofFolder = self.PROOFS_dir+self.dir_separator + self.file[3]  # Solution folder
            zip_file_name = str(self.student[0]) + "_" + self.file[3]+ "_" + str(now_string) +'.zip' # .zip file name

        dir = Path(proofFolder) # Convert to Path object
        fullname = self.ZIP_dir+self.dir_separator+zip_file_name

        try:
            with zipfile.ZipFile(fullname, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for entry in dir.glob("*.sol"): # write all .sol files to the zip file
                    zip_file.write(entry, entry.relative_to(dir))
            zip_file.close()
            message = '<.SOL> FILES IN <PROOF> DIR  \n\nHAVE BEEN COMPRESSED \n\nSUCCESSFULLY!!!' \
                                                 '\n\nThe ZIP file is available \n\nin the folder ZIP.'

            PopupMessage(message, '#33FF33')
        except:
            err_message = 'Cannot write to file: ' + zip_file_name
            PopupMessage(err_message, '#FF33FF')  # cor lilás

        return

    # -----------------------------------------------------------------------------
    def import_list(self, handle, path, filename):
        '''
        Imports a list of problems (arguments) from .TXT file
        Premisses must be separated by by SPACE-COMMMA-SPACE.
        Cojunction operator is & and disjunction operator is | (with spaces before and after them)
        The last proposition must be the conclusion

        Parameters:
            handle: is a handle to the class <InputArgumentBox>, witch has
            the functions inputPremiss and inputConclusion
            path: the path to the file
            filename:
        '''

        print('IMPORTING LIST')
        self.resetApp()
        handle.resetInput()

        if filename == []:
            PopupMessage('Choose a file, please.','#FF33FF') #cor lilás
        else:
            base = os.path.basename(str(filename[0])) # Get only the name of the file
            problemListName = base.split('.')[0] # Get the name of the problem list
            # fName = os.path.splitext(base)[0] # Get the name of the file, without extension

            proofDir = self.PROOFS_dir + self.dir_separator +problemListName # Includes problemListName in the PROOFS dir name
            # print(f'base: {base}')
            # print(f'problemListName: {problemListName}')
            # print(f'profDir: {proofDir}')

            if os.path.isdir(proofDir):
                pass  # The folder named as the problem list name exists already
            else:
                os.mkdir(proofDir)  # Create a folder named as the problem list name

            self.file = (path,"",base,problemListName)
            with open(os.path.join(path, filename[0]), 'r', encoding='utf8') as f:
                self.list_of_problems = f.read().splitlines() # Returns a list of lines

        self.list_of_problems = self.remove_comments(self.list_of_problems)
        # print(f'self.list_of_problems:{self.list_of_problems}')


        popupGetQt = PopupGetOption()
        popupGetQt.options = self.list_of_problems
        popupGetQt.title = 'Select one problem to solve, please.'

        popupGetQt.open()
        popupGetQt.bind(title=partial(self.prove_an_argument,handle,base,problemListName))

        return

    # -----------------------------------------------------------------------------
    def prove_next_problem(self):

        ref = self.ids.input_or_proof_screen.ids.input_screen.ids.in_arg_box

        popupGetQt = PopupGetOption()
        popupGetQt.options = self.list_of_problems
        popupGetQt.title = 'Select one problem to solve, please.'

        popupGetQt.open()

        base = self.file[2]
        newDirName = self.file[3]
        popupGetQt.bind(title=partial(self.prove_an_argument, ref, base,newDirName))
        return

    # -----------------------------------------------------------------------------
    def remove_comments(self, lines):
        '''
            Comments are lines started by the character '#'.
            They must be removed from the input file.
            Empty lines are also removed
        '''

        lines = [l for l in lines if len(l) != 0]
        lines = [l for l in lines if l[0] != '#']
        return lines

    # -----------------------------------------------------------------------------
    def n_prove_an_argument(self,in_box,line):

        print(f'Proving line: {line}')

        print(f'line: {line}')
        # handle = args[0]
        # base = args[1]
        # problemListName = args[2]
        # line = args[4]
        # print(f'base: {base}')
        # print(f'problemListName: {problemListName}')
        # print(f'line: {line}')

        lp = line.split(' - ') # lp = (index, arg)
        print(f'lp: {lp}')

        try:
            index = int(lp[0])
            arg = lp[1]
        except:
            # PopupMessage('Fail in finding an index for a problem.', '#FF33FF')  # cor lilás
            return 'Fail in finding an index for a problem.'

        try:
            arg = arg.replace('|-', fms.GlobalConstants.c_ass)  # Replace '->' by  '⊢'
            # l_terms = arg.split(' |- ')  # Conclusion must appear after ' |- "
            l_terms = arg.split(' '+fms.GlobalConstants.c_ass+' ')  # Conclusion must appear after ' ⊢ "
            print(f'l_terms: {l_terms} - len: {len(l_terms)}')
            s_conclusion = l_terms[1] # l_terms is a list of 2 elements: a string of premisses and a conclusion
            print(f's_conclusion: {s_conclusion}')
            s_premisses = str(l_terms[0])
            print(f's_premisses: {s_premisses}')
            l_premisses = s_premisses.split(' , ') #Premisses must be sepatared by  SPACE-COMMA-SPARE
            print(f'l_premisses: {l_premisses}')
        except:
            #kivy PopupMessage('Error while importing file.', '#FF33FF')  # cor lilás
            return 'Error while importing file.'

        try:
            # Preparing the list of premisses
            for prem in l_premisses:
                print(f'prem antes: {prem}')
                prem = self.insert_spaces(prem)
                print(f'prem depois: {prem}')
                list_prem = prem.split()
                #Variables in predicates must be separeted by COMMAS WHITHOUT spaces between it
                list_prem = list(filter((',').__ne__, list_prem))  # remove all occurences of ',' from the input_string

                in_box.input_l = list_prem
                print(f'in_box.input_l: {in_box.input_l} ')
                print(f'in_box: {in_box} ')
                r, msg = in_box.inputPremiss(str(list_prem))  # Include new premiss
                print('>>>>>inputPremisses ended', msg)

            # Preparing the conclusion

            s_conclusion = self.insert_spaces(s_conclusion)
            list_s_conclusion = s_conclusion.split()
            list_s_conclusion = list(filter((',').__ne__, list_s_conclusion))  # remove all occurences of ',' from the input_string

            in_box.input_l = list_s_conclusion
            r, msg =  in_box.inputConclusion() #Include conclusion
            print('>>>>>inputConclusion ended', msg)
        except:
            # PopupMessage('Error preparing argument.', '#FF33FF')  # cor lilás
            return 'Error preparing argument.'

        print(f'in_box.input_premisses: {in_box.input_premisses} ')
        print(f'in_box.input_conclusion: {in_box.input_conclusion} ')

        self.initProof(in_box.input_premisses, in_box.input_conclusion)

        # ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.input_status_bar.ids.file_label
        # ref.text = "File: " + "pb"+str(index)+"-"+base
        # print("File: " + "pb"+str(index)+"-"+base)
        ###############################################################################
        # self.file = (self.file[0],"pb"+str(index)+"-",base,problemListName) #updates solution file name
        # printf(f'FileName: {self.file}')


        # print(f'self.list_of_problems: {self.list_of_problems} ')

        # self.list_of_problems.remove(line) # Remove the selected problem from the list of problems

        return

    # -----------------------------------------------------------------------------
    def insert_spaces(self,input_string):
        cnt = fms.GlobalConstants()

        input_string = input_string.replace(cnt.fa, ' '+cnt.fa+' ')  # Insert a space before and after 'fa'
        input_string = input_string.replace(cnt.ex, ' '+cnt.ex+' ')  # Insert a space before and after 'ex'
        input_string = input_string.replace(cnt.c_not, ' '+cnt.c_not+' ')  # Insert a space before and after 'not'
        input_string = input_string.replace('&', ' '+cnt.c_and+' ')  # Insert a space before and after ',' (AND)
        input_string = input_string.replace('^', ' '+cnt.c_and+' ')  # Insert a space before and after ',' (AND)
        input_string = input_string.replace('|', ' '+cnt.c_or+' ')  # Insert a space before and after '|' (OR)
        input_string = input_string.replace('v', ' '+cnt.c_or+' ')  # Insert a space before and after '|' (OR)
        input_string = input_string.replace('(', ' ( ')  # Insert a space before and after '('
        input_string = input_string.replace(')', ' ) ')  # Insert a space before and after ')'
        input_string = input_string.replace('~', ' '+cnt.c_not+' ')  # Insert a space before and after '~'
        input_string = input_string.replace('<->', ' '+cnt.c_iff+' ')  # Insert a space before and after '<->'. The previous line
                                                               # changes original occurrences of '<->
        input_string = input_string.replace('->', ' '+cnt.c_if+' ')  # Insert a space before and after '->'
        input_string = input_string.replace(',', ' , ')  # Insert a space before and after ','
        input_string = input_string.replace('T', cnt.true)  # Tautology
        input_string = input_string.replace('C', cnt.false)  # Contradiction
        for c in cnt.list_of_functs:
            input_string = input_string.replace(c, ' '+c)  # Insert a space before a functor symbol

        return input_string

    # -----------------------------------------------------------------------------
    def load(self, path, filename):
        self.resetApp()
        if filename == []:
            PopupMessage('Choose a file, please.','#FF33FF') #cor lilás
        else:
            base = os.path.basename(str(filename[0])) # Get only the name of the file
            fName = os.path.splitext(base)[0] # Get the name of the file, without extension
            self.file = (path,"",fName,'')
            with open(os.path.join(path, filename[0]), 'rb') as stream:
                try:
                    while True:
                        argument = pickle.load(stream)
                        premisses = argument[0]
                        conclusion = argument[1]

                        # Replace ASCII connectives by UTF-8 connectives
                        # premisses, conclusion = convert_argument(premisses,conclusion)

                        self.proof_lines = premisses
                        self.premisses = copy.copy(premisses)
                        self.conclusion = conclusion
                        self.initProof(self.proof_lines,self.conclusion)
                    stream.close()
                except EOFError:
                    pass
                except:
                    PopupMessage('Error while reading file.','#FF33FF') #cor lilás

            print('load()')
            print(f'premisses: {premisses}')
            print(f'conclusion: {conclusion}')

            ref = self.ids.input_or_proof_screen.ids.proof_screen.ids.input_status_bar.ids.file_label
            ref.text = "File: "+base

    # -----------------------------------------------------------------------------
    # def convert_symbols(self, premisses,conclusion):
    #     """ Replace textual symbols for connectives in argument
    #         by corresponding UTF-8 GlobalConstants symbols
    #     """
    #     n_premisses = []
    #     for f in premisses:
    #         # print(f'premiss: {f}')
    #         p = self.convert_symbols(f)
    #         # print(f'new_premiss: {p}')
    #         n_premisses.append(p)
    #     n_conclusion = self.convert_symbols(conclusion)
    #
    #     return n_premisses, n_conclusion
    #
    # # -----------------------------------------------------------------------------
    # def convert_symbols(self, formula):
    #     # print(f' formula: {formula}: type: {type(formula)}')
    #     if type(formula) is fms.Form:
    #         return formula
    #     elif type(formula) is fms.Form0:
    #         return formula
    #     elif type(formula) is fms.Form1:
    #         nOpnd1 = self.convert_symbols(formula.getOpnd1())
    #         # print(f'nOpnd1_f1: {nOpnd1}')
    #         n_form = fms.Form1(fms.GlobalConstants.c_not,nOpnd1)
    #         # print(f'n_form: {n_form}')
    #         return n_form
    #     elif type(formula) is fms.Form2:
    #         opnd1 = formula.getOpnd1()
    #         # print(f'opnd1: {opnd1}')
    #         nOpnd1 = self.convert_symbols(opnd1)
    #         # print(f'nOpnd1: {nOpnd1}')
    #         opnd2 = formula.getOpnd2()
    #         # print(f'opnd2: {opnd2}')
    #         nOpnd2 = self.convert_symbols(opnd2)
    #         # print(f'nOpnd2: {nOpnd2}')
    #         oper = formula.getOper()
    #         # print(f'oper: {oper}')
    #
    #         if oper == '^': oper = fms.GlobalConstants.c_and
    #         if oper == 'v': oper = fms.GlobalConstants.c_or
    #         if oper == '->': oper = fms.GlobalConstants.c_if
    #         if oper == '<->': oper = fms.GlobalConstants.c_iff
    #         # print(f'noper: {oper}')
    #         new_form = fms.Form2(nOpnd1,oper,nOpnd2)
    #         # print(f'new_form: {new_form}')
    #         return new_form
    #     else:
    #         return formula

    # -----------------------------------------------------------------------------
    def save(self, path, filename):
        content = (self.proof_lines, self.conclusion) # Content to save

        if filename == []:
            PopupMessage('Choose a file, please.','#FF33FF') #cor lilás
        else:
            if os.path.isfile(filename):
                self.confirm_overwriting(path, filename, content)
            else:
                self.write_to_file( path, filename, content)
        return

    # -----------------------------------------------------------------------------
    def confirm_overwriting(self,path, filename, content):
        # create content and add to the popup
        layout = BoxLayout()
        yes_but = Button(text='Yes')
        no_but = Button(text='No')
        layout.add_widget(yes_but)
        layout.add_widget(no_but)
        popup = Popup(title='File <'+filename+'> exists. Overwrite? (y/n) ', content=layout,
                      auto_dismiss=False, size_hint=(.9, .4))

        # bind the on_press event of the button to the dismiss function

        # yes_but.bind(state=partial(self.callback, x='True'))
        yes_but.bind(on_press=lambda x: self.on_press(popup, path, filename, content))
        # yes_but.bind(on_press=self.callback)
        no_but.bind(on_press=popup.dismiss)
        popup.open()

        return

    # -----------------------------------------------------------------------------
    def on_press(self,popup, path, filename, content):
        self.write_to_file(path, filename, content)
        popup.dismiss()

    # -----------------------------------------------------------------------------
    def write_to_file(self, path, filename, content):
        try:
            # base = os.path.basename(str(filename))  # Get only the name of the file
            # fName = os.path.splitext(base)[0] # Get the name os the file,
            # self.file = (path,"",fName,'')
            with open(os.path.join(path, filename), 'wb') as stream:
                # argument = (self.proof_lines, self.conclusion)
                # pickle.dump(argument, stream)
                pickle.dump(content, stream)
        except:
            err_message = 'Cannot write to file: ' + filename
            PopupMessage(err_message, '#FF33FF')  # cor lilás
        return

    # -----------------------------------------------------------------------------
    def write_encrypted_to_file(self, path, filename, content):
        try:
            # base = os.path.basename(str(filename))  # Get only the name of the file
            # fName = os.path.splitext(base)[0] # Get the name os the file,
            # self.file = (path,"",fName,'')
            with open(os.path.join(path, filename), 'wb') as stream:
                # argument = (self.proof_lines, self.conclusion)
                # pickle.dump(argument, stream)
                pickle.dump(content, stream)
        except:
            err_message = 'Cannot write to file: ' + filename
            PopupMessage(err_message, '#FF33FF')  # cor lilás
        return


    # -----------------------------------------------------------------------------
    def saveSolution(self, solution_status):

        if solution_status == 'FINAL':
            ext = '.sol'
        else:
            ext = '.prt'

        ptable = PrettyTable(["Index", "Formula", "Rules"])
        # Align columns

        ptable.align["Index"] = "l"
        ptable.align["Formula"] = "l"
        ptable.align["Rules"] = "l"
        # Keep a space columns edge and content (default)
        ptable.padding_width = 1
        line = 0
        # while line < self.lineIndex:
        while line < len(self.premisses):
            indstr = '(' + str(line) + ')'
            ptable.add_row([indstr, self.proof_lines[line], 'P'])
            line += 1

        ptable.add_row(['-----', '------------------------', '-------------'])
        for line in self.line_stack:
            indstr = '(' + line[1].text + ')'
            ptable.add_row([indstr, line[2].text, line[3].text])

        table_txt = ptable.get_string()
        performance = '\n Time: ' + str(self.time) + ' (s) - Errors: ' + str(self.errors) + ' (s) - Backs: ' + str(self.backs)
        time = datetime.now()
        # print(f'self.file: {self.file}')
        problemName = self.file[2].split('.')[0] # The base name of the file
        folderName = self.file[3]
        if folderName == '':
            path = self.PROOFS_dir
        else:
            path = self.PROOFS_dir+self.dir_separator+folderName

        filename = str(self.student[0])+"_"+str(self.file[1])+str(problemName)+ ext
        # print(f'filename: {filename}')
        # print(f'self.file: {self.file}')

        solution = (self.student, time, path, filename, performance, table_txt)

        if os.path.isfile(path+self.dir_separator+filename): # Check if file exists
            self.confirm_overwriting(path, filename, solution)
        else:
            self.write_to_file(path, filename, solution)
            # self.encrypt_solution(path,filename)
            # self.write_encrypted_to_file(path, filename, e_solution)

        return

    # -----------------------------------------------------------------------------
    # def encrypt_solution(self,path,filename):
    #
    #     # opening the key
    #     with open(os.path.join(path, 'mrplato.ky'), 'rb') as filekey:
    #         key = filekey.read()
    #
    #     # using the key
    #     fernet = Fernet(key)
    #
    #     # opening the original file to encrypt
    #     with open(os.path.join(path,filename), 'rb') as file:
    #         original = file.read()
    #
    #     # encrypting solution
    #     encrypted_sol = fernet.encrypt(original)
    #
    #     # write encrypted file
    #     with open(os.path.join(path,filename), 'wb') as encrypted_file:
    #         print('encrypting')
    #         encrypted_file.write(encrypted_sol)

        return

    # -----------------------------------------------------------------------------
    def printProofTable(self):
        '''
           Print a table of proof lines

        '''

        ptable = PrettyTable(["Index", "Formula", "Rules"])
        # Align columns

        ptable.align["Index"] = "l"
        ptable.align["Formula"] = "l"
        ptable.align["Rules"] = "l"
        # Keep a space columns edge and content (default)
        ptable.padding_width = 1
        line = 0

        for p in self.premisses:
            indstr = '(' + str(line) + ')'
            ptable.add_row([indstr, p, 'P'])
            line += 1

        ptable.add_row(['-----', '------------------------', '-------------'])
        for line in self.line_stack:
            indstr = '(' + line[1].text + ')'
            ptable.add_row([indstr, line[2].text, line[3].text])

        table_txt =  ptable.get_string()
        performance = '\n Time: '+str(self.time) +' (s) - Errors: '+str(self.errors) + ' (s) - Backs: ' + str(self.backs)
        now = datetime.now()
        now_string = now.strftime("%d_%m_%Y-%H_%M")
        # print(f'time: {now}')
        filename = "outputProof"+str(now_string)+'.prf'
        try:
            with open(filename,"w") as file:
                file.write(table_txt)
                file.write(performance)
        except:
            err_message = 'Cannot write to file: '+filename
            PopupMessage(err_message,'#FF33FF') #cor lilás

        print(ptable)

        return

# -----------------------------------------------------------------------------
class popupConfirmationDialog():

    def __init__(self):
        self.answer = 'nada'
        # create content and add to the popup
        layout = BoxLayout()
        yes_but = Button(text='Yes')
        no_but = Button(text='No')
        layout.add_widget(yes_but)
        layout.add_widget(no_but)
        popup = Popup(title='File exists. Overwrite? (y/n) ', content=layout,
                       auto_dismiss=False, size_hint=(.9, .4))

        # bind the on_press event of the button to the dismiss function

        # yes_but.bind(state=partial(self.callback, x='True'))
        yes_but.bind(on_press = lambda x: self.on_press(popup,x='True'))
        # yes_but.bind(on_press=self.callback)
        no_but.bind(on_press=popup.dismiss)
        popup.open()

    # -----------------------------------------------------------------------------
    def on_press(self,popup, x):
        print("on_press: x=", x)
        self.answer = x
        popup.dismiss()

    # -----------------------------------------------------------------------------
    def get_answer(self):
        return(self.answer)


# If you want to dynamically change the title, you can do:
#
# from kivy.base import EventLoop
# EventLoop.window.title = 'New title'

# -----------------------------------------------------------------------------
# if __name__ == '__main__':
#     MrPlatoApp().run()


pw = ProofWindow()
# pw.resetApp()
in_box = InputArgumentBox()

#PROVANDO INFERÊNCIAS
# print('PROVANDO INFERÊNCIAS')
#
#
# list_of_problems = ['1 - p → q , p ⊢ q', '2 - p → q , ~q ⊢ ~p', '3 - p → q , q → s ⊢ p → s']
# line = list_of_problems[2] # problema selecionado
# sel_rule = 42 # regra selecionada
# sel_lines = [0,1] # linhas de prova selecionadas
#
#
# pw.selected_lines = sel_lines
# pw.selected_rule_index = ('INF', sel_rule)
# pw.infCheckBox = sel_rule
#
# in_box = InputArgumentBox()
#
# pw.n_prove_an_argument(in_box,line)
# print('APLYING THE RULE')
#
# r, msg = pw.appRule()
# print(f'r:{r}')
# if r:
#     print('Processing ended with success!')
#     print(f'partial conclusion: {msg}')
# else:
#     print('PROCESSING ENDED WITH UNSUCESS!')
#     print('DIAGNOSYS: ',msg)

# PROVANDO EQUIVALÊNCIAS

#selecionando a parte onde será aplicada a regra de equivalềncia

# list_of_problems = ['1 - ~~p → q ⊢ p -> q', '2 - p → ~~q ⊢ p -> q', '3 - p → ~(p ^ r)  ⊢ p →  (~p v ~r)','4 - ~~p ⊢ p']
#
# line = list_of_problems[1] # problema selecionado
#
# sel_rule = 42 # regra selecionada
# sel_lines = [0] # linhas de prova selecionadas
#
# pw.selected_lines = sel_lines
# pw.selected_rule_index = ('EQ', sel_rule)
# pw.infCheckBox = sel_rule
#
# #handle.resetInput()
# # self.list_of_problems = self.remove_comments(self.list_of_problems)
# pw.n_prove_an_argument(in_box,line)
#
# print('APLYING THE RULE')
# r, msg = pw.appRule()
# print(f'r:{r}')
# if r:
#     print('Processing ended with success!')
#     print(f'partial conclusion: {msg}')
# else:
#     print('PROCESSING ENDED WITH UNSUCESS!')
#     print('DIAGNOSYS: ',msg)


#selecionando somente uma parte da  linha
# print('Selecionando somente uma parte da  linha')

#list_of_problems = ['1 - ~~p → q ⊢ p -> q', '2 - p → ~~q ⊢ p -> q', '3 - p → ~(p ^ r)  ⊢ p →  (~p v ~r)','4 - ~~p ⊢ p']

# pw.n_prove_an_argument(in_box,line)

# ind_form_list = fms.index_form(0, pw.proof_lines[0])
# print(f'ind_form_list: {ind_form_list}')
# options = pw.get_options(ind_form_list)
# print(f'options: {options}')
# selOption = options[1]
# print(f'selOption: {selOption}')

# Chamar  <getSelectedSubFormula2>

# print(f'proof_lines[0]: {pw.proof_lines[0]}')
# newLine = pw.getSelectedSubFormula2(selOption, str(pw.proof_lines[0]))
# print(f'Newline: {newLine}')

# use_kivy_settings = True
# If True, the application settings will also include the Kivy settings. If you don’t want the user to change any kivy settings from your settings UI, change this to False.
#
# property user_data_dir


#inserindo nova hipótese
# list_of_problems = ['1 - p → q , q → r  ⊢ p -> r']
# line = list_of_problems[0] # problema selecionado

# sel_rule = 0 # regra selecionada ADHYP
# sel_lines = [0] # linhas de prova selecionadas

# pw.selected_lines = sel_lines
# pw.selected_rule_index = ('INF', sel_rule)
# pw.infCheckBox = sel_rule

# pw.n_prove_an_argument(in_box,line)
# inForm = InputAdditionalForm()
# inForm.input_l = ['p'] # hypótese inserida pelo usuário

# print('APLYING THE RULE')
# r, newHypothesys = inForm.inputAditionalFormulaOrHyphotesis(pw)
# print(f'NewHYp: {newHypothesys}')

# if r:
#     print('Processing ended with success!')
# else:
#     print('PROCESSING ENDED WITH UNSUCESS!')
#     print('DIAGNOSYS: ',msg)

#Removendo uma hipótese