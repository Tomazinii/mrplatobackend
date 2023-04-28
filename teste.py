# import re

# # Define a expressão regular para o formato esperado das linhas
# regex = r'^\d+ - '

# # Abre o arquivo txt para leitura
# with open('lista0.txt', 'r') as file:
#     # Lê cada linha do arquivo
#     for line in file:
#         # Remove espaços em branco no começo e no fim da linha
#         line = line.strip()
#         # Verifica se a linha está no formato correto
#         if not re.match(regex, line):
#             print(f'A linha "{line}" não está no formato correto.')



with open("lista0.arg","r",encoding="utf-8") as txt:
    array = txt.readlines()

print(array)