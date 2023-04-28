import re

class FileExercise:
    __file: list

    def __init__(self, file):
        self.__file = file


    @staticmethod
    def create(file: list):
        erro = FileExercise.validar_lista(file)
        if erro:
            raise ValueError(erro)
        
        return FileExercise(file=file)

    @staticmethod
    def validar_linha(linha, num_linha):
        padrao = r'^\d+ - '
        
        if not re.match(padrao, linha.strip()):
            return f'Linha {num_linha}: {linha}'
        else:
            return None
        
    @staticmethod   
    def validar_lista(lista):
        for i, linha in enumerate(lista):
            erro = FileExercise.validar_linha(linha, i + 1)
            if erro:
                return erro
        return None

    def get_list(self):
        return self.__file