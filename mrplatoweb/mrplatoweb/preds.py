#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 10:37:10 2021

@author: Cedric Luiz de Carvalho
"""

class Quantifier:
    '''
    Defines a class for logic formulas with only propositional symbols.
    An atomic proposition: a letter from the end of alphabet (p,q,r,...)

    Argument: opnd1
    '''
    def __init__(self, type, var):
        self.type = type
        self.var = var

    # def __eq__(self, other):
    #     if type(other) is not Form:
    #         return False
    #     else:
    #         return self.opnd1 == other.opnd1
        
    # def __str__(self):      #Form to string
    #    return  self.opnd1
    
    def __str__(self):         # Form to string
        return '{self.type}({self.var})'.format(self=self)
 
    def setVar(self, var): # Sets a new operand (a value)
        self.var = var
            
    def getVar(self): # Gets the operand of a Form
        return self.var
# -----------------------------------------------------------------------------


class Form:
    '''
    Defines a class for logic formulas with only propositional symbols.
    An atomic proposition: a letter from the end of alphabet (p,q,r,...)

    Argument: opnd1
    '''

    def __init__(self, opnd1):
        self.opnd1 = opnd1

    def __eq__(self, other):
        if type(other) is not Form:
            return False
        else:
            return self.opnd1 == other.opnd1

    # def __str__(self):      #Form to string
    #    return  self.opnd1

    def __str__(self):  # Form to string
        return '{self.opnd1}'.format(self=self)

    def setOpnd1(self, opnd1):  # Sets a new operand (a value)
        self.opnd1 = opnd1

    def getOpnd1(self):  # Gets the operand of a Form
        return self.opnd1
# -----------------------------------------------------------------------------

# q1 = Quantifier('fa','x')
# print(f'q1: {q1}')

class Form0(Form):
    '''
    Defines the constants T (tautology) and
    C (contradiction)

    Extends Form.

    Argument: opnd1
    '''

    def __init__(self, opnd1):
       Form.__init__(self, opnd1)

    def __eq__(self, other):  # Checks equivalence of two Form1 objects
        if type(other) is not Form0:  # The other object must be Form0
            return False
        else:  # Operands of both objects must be igual
            return self.opnd1 == other.opnd1

    def __str__(self):  # Form0 to string
       return '{self.opnd1}'.format(self=self)
#
# class Form1(Form):
#     '''
#     Defines negation of a proposition.
#     The operation must always be (~).
#     The operand must be a logic formula.
#
#     Extends Form.
#
#     Argument: opnd1
#     '''
#
#     oper = '~'    # Negation is an operation with just one argument
#
#     def __init__(self, oper, opnd1):
#         Form.__init__(self, opnd1)
#
#     def __eq__(self, other): # Checks equivalence of two Form1 objects
#         if type(other) is not Form1: # The other object must be Form1
#             return False
#         else: # Operands of both objects must be igual
#             eqs = (self.oper == other.oper) & (self.opnd1 == other.opnd1)
#             return eqs
#
#     def __str__(self):         # Form1 to string
#         if type(self.opnd1) is Form2: # Negation of a Form2 object is printed between parenthesis
#             return '~ ( {self.opnd1} )'.format(self=self)
#         else:
#             return '~ {self.opnd1}'.format(self=self)
#
#
#     def getOper(self):
#         return self.oper    # Gets operator (~)
#
# # -----------------------------------------------------------------------------
#
#
# class Form2(Form1):
#     '''
#     Defines composed formulas, with the operands conected
#     by one of the operators (^ v -> <->).
#
#     Extends Form1.
#
#     Arguments: opnd1 and opnd2
#     '''
#
#     def __init__(self, opnd1, oper, opnd2):
#             Form1.__init__(self, oper, opnd1 )
#             self.oper = oper
#             self.opnd2 = opnd2
#
#     def __eq__(self, other):
#         if type(other) is not Form2: # The other object must be Form2
#             return False
#         else:
#             eqs = (self.oper == other.oper) & (self.opnd1 == other.opnd1) & (self.opnd2 == other.opnd2)
#             return eqs
#
#     def __str__(self):       # Form2 to string
#
#             if (type(self.opnd1) is Form2) & (type(self.opnd2) is Form2):
#                 return '({self.opnd1}) {self.oper} ({self.opnd2})'.format(self=self)
#             elif type(self.opnd1) is Form2:
#                 return '({self.opnd1}) {self.oper} {self.opnd2}'.format(self=self)
#             elif type(self.opnd2) is Form2:
#                 return '{self.opnd1} {self.oper} ({self.opnd2})'.format(self=self)
#             else:
#                 return '{self.opnd1} {self.oper} {self.opnd2}'.format(self=self)
#
#     def setOper(self, oper):
#             self.oper = oper
#
#     def getOper(self):
#             return self.oper
#
#     def setOpnd2(self, opnd2):
#             self.opnd2 = opnd2
#
#     def getOpnd2(self):
#             return self.opnd2
#
# # -----------------------------------------------------------------------------
#
#
# def new_Formula(args):
#     '''
#       Creates a new logic formula.
#
#     :param args: a logic formula (a string).
#     :return: a logic formula object - Form*
#     '''
#
#     if args[0] == '~':
#         form0 = new_Formula(args[1])
#         form = Form1('~', form0)
#     elif len(args) > 2 and args[1] in ['^','v','->',',<->']:
#         form0 = new_Formula(args[0])
#         form1 = new_Formula(args[2])
#         form = Form2(form0, args[1], form1)
#     else:
#         form = Form(args[0])
#
#     return form
#
# # -----------------------------------------------------------------------------
#
#
# def updateDic(dic,index,value):
#     '''
#         Updates variable mapping. If a variable is in the dictionary
#         already, its value must be the same new value to be associated
#         to it, otherwise unification fails.
#
#     :param dic: the variables/values mapping.
#     :param index: the key (variable name).
#     :param value: value
#     :return unify: a boolean, dic: variable mapping.
#     '''
#
#     if index in dic:
#         if dic[index] != value:
#             unify = False
#         else:
#             unify = True
#     else:
#         dic[index] = value
#         unify = True
#     return unify, dic
#
# # -----------------------------------------------------------------------------
#
#
# def unify(initDic,formula1,formula2):
#     '''
#         Checks if two logic forms unify, updating the variable mapping.
#
#         :param initDic: the variables/values mapping.
#         :param formula1: A formula to be unified.
#         :param formula2: A formula to be unified.
#         :return (1) A boolean (False, if formulas do not unify).
#                 (2) The updated mapping (a dictionary).
#
#                 Ex.: (p -> q) e (a -> b) produces the mapping {p:a, q:b}
#     '''
#     # print(f'formula1: {formula1} <{type(formula1)}>, formula2: {formula2}<{type(formula2)}>')
#
#     if (type(formula1) is Form0) & (type(formula2) is Form0):  # Constants
#         r_unify = formula1.getOpnd1() == formula2.getOpnd1()
#         return r_unify, initDic
#     elif (type(formula1) is Form) & (type(formula2) is Form):  # Atomic formulas
#         r_unify, newDic = updateDic(initDic, formula1.getOpnd1(), formula2.getOpnd1())
#         return True & r_unify, newDic
#     elif(type(formula1) is Form) & (type(formula2) is Form0):  # A variable and a constant (T or C)
#         r_unify, newDic = updateDic(initDic, formula1.getOpnd1(), formula2)
#         return True & r_unify, newDic
#     elif (type(formula1) is Form) & (type(formula2) is Form1):  # p => ~a produces  {p:~a}
#         r_unify, newDic = updateDic(initDic,formula1.getOpnd1(),formula2)
#         return True & r_unify, newDic
#     elif (type(formula1) is Form) & (type(formula2) is Form2):  # p => a ^ b produces  {p:a ^ b}
#         r_unify, newDic = updateDic(initDic,formula1.getOpnd1(),formula2)
#         return True & r_unify, newDic
#     elif (type(formula1) is Form1) & (type(formula2) is Form):  # ~p => a produces {p:~a}
#         nformula2 = Form1('~',formula2) #  Denies formula 2
#         f1_opnd1 = formula1.getOpnd1()
#         if type(f1_opnd1) is Form1: # ~~p => a produces {p:~~a}
#             r, newDic = unify(initDic, f1_opnd1.getOpnd1(),  Form1('~',nformula2))
#         else:
#         # print(f'f1.opnd1: {formula1.getOpnd1()} - {type(formula1.getOpnd1())}>, f2.opnd1: {formula2.getOpnd1()}- {type(formula2.getOpnd1())}>')
#             r, newDic = unify(initDic, formula1.getOpnd1(),nformula2 )
#         return r & True, newDic
#     elif (type(formula1) is Form1) & (type(formula2) is Form1):  # Negations
#         r, newDic = unify(initDic, formula1.getOpnd1(),formula2.getOpnd1() )
#         return r & True, newDic
#     elif (type(formula1) is Form2) & (type(formula2) is Form2):
#         if formula1.getOper() == formula2.getOper(): # cond., bicond., conj. e disj.
#             r1, newDic = unify(initDic, formula1.getOpnd1(),formula2.getOpnd1() )
#             # print(f'f1.opnd2: {formula1.getOpnd2()} - {type(formula1.getOpnd2())}>, f2.opnd2: {formula2.getOpnd2()} - {type(formula2.getOpnd2())}>')
#             r2, newDic2 = unify(newDic, formula1.getOpnd2(),formula2.getOpnd2() )
#             return r1 & r2 & True, newDic2
#         else:
#             return False, initDic
#
#     else:
#         return False, initDic
#
# # ----------------------------------------------------------------------------
#
#
# # f01 = Form('p')
# # f02 = Form('a')
# # f03 = Form('q')
# # f04 = Form('b')
# #
# # f11 = Form1('~',f01)
# # f13 = Form1('~',f03)
# # #
# # f21 = Form2(f01,'v',f11)
# # f22 = Form2(f03,'v',f13)
# #
# #
# # f51 = Form2(f03,'^',Form0('T'))
# # f51 = Form2(f03,'^',Form0('T'))
# #
# # r, dic = unify({}, f21, f22)
# # print(f'r: {r}')
# #
# # for d in dic:
# #     print(f'dic[{d}] : {dic[d]}')
# #
# # print(f'r : {r}')
#
# # f31 = Form2(f01,'v',f03)
# # f32 = Form2(f02,'v',f04)
#
# # g01 = Form1('~',f21)
# # g02 = Form1('~',f22)
#
#
# # r, dic = unify({}, f51, f51)# for d in dic:
# # for d in dic:
# #     print(f'dic[{d}] : {dic[d]}')
# # print(f'r: {r}')
#
# # -----------------------------------------------------------------------------
#
#
# def print_mapeamento(dic):
#     print("contexto: {")
#     for key, value in dic.items():
#         print('(', key, ': ', value,')')
#     print("}")
#
# # -----------------------------------------------------------------------------
#
#
# def generate_represent(form):
#     '''
#         Generates a representation for a formula (a string).
#         Produces FORM* objects.
#
#     :param form: a formula (a string).
#     :return (1) r: a boolean (False if representation can not be constructed),
#             (2) err_message: an error message in case r is False.
#             (3) A new formula (Form*) if possible, or None otherwise.
#     '''
#     l = len(form)
#     # print(f'form to represent: {form} - len {l}')
#     if l == 0:
#         err_message = 'Error: wrong form.'
#         return False, err_message, None
#     elif (l == 1) & (form[0] in [ '~','^','v','->','<->']):  # Those operations must have an operand
#         err_message = 'Error: an operand is missing.'
#         return False, err_message, None
#     elif (l == 1) & (form[0] in [ 'T','C']):  # Constants
#         return True, '', Form0(form)
#     elif (l == 1) & (form[0] in ['p', 'q', 'r', 's', 't','u']):  # Those operations must have an operand
#         return True, '', Form(form)
#     elif (l == 1) & (form[0] in ['T', 'C']):  # Constants
#         return True, '', Form0(form)
#     elif (l == 1):
#         err_message= 'Error: wrong formula.'
#         return False, err_message, None
#     elif (l == 2) & (form[0] in [ '^','v','->','<->']):  # Those operations must have two operands
#         err_message = 'Error: the first operand is missing.'
#         return False, err_message, None
#     elif (l == 2) & (form[0] == '~'):
#         r, err_message, opnd1 = generate_represent(form[1])
#         nf = Form1('~',opnd1)
#         return r, err_message, nf
#     elif (l == 2):
#         err_message= 'Error: wrong formula'
#         # print(f'rp: {err_message} ')
#         return False, err_message, None
#     else: # In case l > 2 : the main operator should be in ['^','v','->','<->']
#         r, err_message, oper, opnd1,opnd2 = handle_precedence_of_operators(form)
#         # print(f'rp: {r} - opnd1: {opnd1} - opnd2:{opnd2}')
#         if r :
#             if oper == '~': # The main operation is the negation
#                 r, err_message, r_opnd1 = generate_represent(opnd1)
#                 return r, err_message, Form1('~', r_opnd1)
#             else:
#                 r, error_message, r_opnd1 = generate_represent(opnd1)
#                 # print(f'r: {r}- error - {error_message}')
#                 if r:
#                     r, error_message, r_opnd2 = generate_represent(opnd2)
#                     if r:
#                         return r, error_message, Form2(r_opnd1, oper, r_opnd2)
#                     else:
#                         err_message= 'Error: the second operand is missing.'
#                         return r, err_message, None
#                 else:
#                     err_message: 'Error: the first operand is missing.'
#                     return r, err_message, None
#         else:
#             return r, err_message, None
#
#
# # -----------------------------------------------------------------------------
#
#
# def handle_precedence_of_operators(form):
#     """
#         Handle precedence of operators, according to the sequence (~,^,v,->,<->).
#         Traverses the string looking for the main operator. After this, looks
#         for the left and right operands.
#
#     :param form: a logic formula (string)
#     :return: a logic formula : operand1 operator operand2
#     """
#     # print(f'form: {form} -  type : {type(form)}')
#     first_occur = {}
#     # O teste dos operandos deve vir aqui na ordem inversa da precedência
#     if '<->' in form: # Gets position of the main operator
#         first_occur['<->'] = form.index('<->')
#     if '->' in form:
#         first_occur['->'] = form.index('->')
#     if 'v' in form:
#         first_occur['v']= form.index('v')
#     if '^' in form:
#         first_occur['^'] = form.index('^')
#
#     if len(first_occur) == 0:
#         if form[0] == '~':
#             r = True
#             err_message = ''  # No error message
#             first_oper = '~'
#             opnd1 = form[1:]
#             opnd2 = form[1:]
#             return r, err_message, first_oper, opnd1, opnd2
#         else:
#             first_oper = ''
#             opnd1 = ''
#             opnd2 = ''
#             r = False
#             err_message= 'Operand is missing!'
#             return r, err_message, first_oper, opnd1, opnd2
#     else:
#         opers = list(first_occur)
#         first_oper = opers[0]
#         position = first_occur[first_oper]
#         # print(f'first_oper: {first_oper} at position: {position}')
#         if position == 1: # First operand is a single variable
#             opnd1 = form[0]
#         else:
#             opnd1 = form[:position]
#
#         if len(form) - (position+1) == 1:  # Second operand is a single variable
#             opnd2 = form[position + 1]
#         else:
#             opnd2 = form[position + 1:]
#
#         r = True
#         # err_message = 'Error handling precedence of operators.'
#         err_message = ''
#
#         return r, err_message, first_oper, opnd1, opnd2
#
# # -----------------------------------------------------------------------------
#
#
# def generate_list_represent(listOfForms):
#     '''
#         Generates a list of FORM* objects from a list o formulas
#
#     :param listOfForms: a list of formulas (strings)
#     :return r: a boolean, mes: an error message, formsRepr: a representarion
#         for the formulas.
#     '''
#
#     formsRepr =[]  # Linhas de prova codificadas
#     i = 0
#     while i < len(listOfForms):
#         r, mes, form = generate_represent(listOfForms[i])
#         if r:
#             formsRepr.append(form)
#             i+=1
#         else:
#             break
#     return r, mes, formsRepr
#
# # ---------------------------------------------------------------------------
#
#
# # f=generate_represent((('~','p'),'^',( '~','q')))
# # print(f)
#
# # p1 = Form1('~', Form('p'))
# # p2 = Form1('~', Form('p'))
# #
# # print(p1 == p2)
#
# # form = ('p', '->', ('q', '->', 'r'))
# # f= generate_represent(form)
# # print(f)