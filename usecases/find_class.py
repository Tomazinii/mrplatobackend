from typing import Type
from interfaces.repository import ClassRepository as ClassRepositoryInterface
from domain.entities.Class import Class

class FindClass:

    def __init__(self, repository: ClassRepositoryInterface):
        self.repository = repository

    
    def find(self, id: int) -> Class:
        if isinstance(id, int):
            obj = self.repository.find(id)
        return obj