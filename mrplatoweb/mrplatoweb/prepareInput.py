#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:04:34 2021

@author: cedric
"""

def prepareInput(t_list):
    if t_list == []:
        return t_list
    elif t_list.count('(') != t_list.count(')'):
        print('Diferent number of ( and )!!')
        return([])
    elif (t_list.count('(') == 0) or (t_list.count(')') == 0):
        print('Diferent number of ( and )!!')
        return([])
    else:
        first_occr = t_list.index(')') # Primeira ocorrência de )
        r_list =  t_list[first_occr::-1]
        # última ocorrência de ( antes do primeiro )
        last_occr = r_list.index('(') 
        print(f'r_list: {r_list}')
        print(f'last_occr: {last_occr} - first_occr: {first_occr}')
        sub_list = t_list[first_occr-last_occr+1:first_occr]
        print(f'sub_list: {sub_list}')
        print(f'a_list: {t_list}')
        del(t_list[first_occr-last_occr:first_occr+1])
        print(f'd_list: {t_list}')
        if len(sub_list) > 1:
            t_list.insert(first_occr-last_occr,sub_list)
        else: 
            t_list.insert(first_occr-last_occr,sub_list[0])
        print(f't_list: {t_list}')
        prepareInput(t_list)
        return t_list
        
        
l = ['(','~','p',')','a','(','p', '^','q',')','(','s', '->','t',')']
print(prepareInput(l))