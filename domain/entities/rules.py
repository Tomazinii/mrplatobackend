from typing import TextIO

class VerifyTxtFileFormat():
    """ this rule verify if txt format is valid """

    @staticmethod
    def verify(self, file: TextIO) -> bool:
        pass

    @staticmethod
    def transform_txt_to_list(self, file: TextIO) -> list:
        pass