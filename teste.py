
import re
import os
from typing import TextIO




# import re

# def validar_linha(linha, num_linha):
#     padrao = r'^\d+ - [A-Za-z]+\s[A-Za-z]+ - \d+ - [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            
#     if not re.match(padrao, linha.strip()):
#         return f'Linha {num_linha}: {linha}'
#     else:
#         return None

# def validar_arquivo(arquivo):
#     with open(arquivo, 'r') as f:
#         linhas = f.readlines()
        
#         for i, linha in enumerate(linhas):
#             erro = validar_linha(linha, i + 1)
            
#             if erro:
#                 return erro
        
#         return True
    

# def validar_arquivo(arquivo):
    
#     # with open(arquivo, 'r') as f:
#     #     linhas = f.readlines()
        
#         for linha in arquivo:
#             padrao = r'^\d+ - [A-Za-z]+\s[A-Za-z]+ - \d+ - [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            
#             if not re.match(padrao, linha.strip()):
#                 return False
        
#         return True
    
# with open("user.txt") as txt:
#     l = txt.readlines()


# print(l)
# print(validar_arquivo(l))


import re

def validar_linha(linha, num_linha):
    padrao = r'^\d+ - [A-Za-z]+\s[A-Za-z]+ - \d+ - [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    
    if not re.match(padrao, linha.strip()):
        return f'Linha {num_linha}: {linha}'
    else:
        return None

def validar_lista(lista):
    for i, linha in enumerate(lista):
        erro = validar_linha(linha, i + 1)
        
        if erro:
            return erro
        
    return None

with open("user.txt") as txt:
    lista = txt.readlines()
    erro = validar_lista(lista)

if erro:
    print(f'A lista não está no formato correto:')
    print(erro)
else:
    print(f'A lista está no formato correto.')