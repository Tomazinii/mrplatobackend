from abc import ABC, abstractmethod
from typing import TextIO

class VerifyTxtFileFormatInterface(ABC):

    @abstractmethod
    def verify(self, file: TextIO):
        raise Exception("Method not implemented")
    
    @abstractmethod
    def transform_txt_to_list(self, file):
        raise Exception("Method not implemented")

