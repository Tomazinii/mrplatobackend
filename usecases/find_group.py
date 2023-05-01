

from typing import Type
from interfaces.repository import GroupRepositoryInterface
from interfaces.use_case import FindGroupInterface
from domain.entities.tournamment import Group

class FindGroup(FindGroupInterface):

    def __init__(self, repository: Type[GroupRepositoryInterface]):
        self.repository = repository

    def find(self, id: int) -> Group:
        if isinstance(id,int):
            response = self.repository.find(id)
            return response
        raise ValueError("invalid format")
