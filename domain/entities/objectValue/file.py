import re


class File:
    __file: list

    def __init__(self, file):
        self.__file = file

    @staticmethod
    def create(file: list):
        erro = File.validar_lista(file)
        if erro:
            raise ValueError(erro)
        
        return File(file=file)
    


    @staticmethod
    def validar_linha(linha, num_linha):
        padrao = r'^\d+ - [A-Za-z]+\s[A-Za-z]+ - \d+ - [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        
        if not re.match(padrao, linha.strip()):
            return f'Linha {num_linha}: {linha}'
        else:
            return None
        
    @staticmethod   
    def validar_lista(lista):
        for i, linha in enumerate(lista):
            erro = File.validar_linha(linha, i + 1)
            
            if erro:
                return erro
            
        return None
    
    def get_file(self):
        return self.__file