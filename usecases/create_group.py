from typing import Type
from interfaces.repository import GroupRepositoryInterface
from interfaces.use_case import CreateGroupInterface
from domain.entities.tournamment import Group
from interfaces.use_case import FindClassInterface

class CreateGroup:

    def __init__(self, repository: Type[GroupRepositoryInterface], use_case_support: Type[FindClassInterface]):
        self.repository = repository
        self.usecase = use_case_support


    def create(self, turma: int, name: str):
        entitie = Group.create(turma, name)

        if isinstance(entitie, Group):
            turma = self.usecase.find(entitie.turma)
            if turma:
                name_obj = entitie.name
                slug = entitie.slug.get_slug()
                exec = self.repository.add(turma=turma[0],name=name_obj, slug=slug)
                
                return exec
            
            raise ValueError("turma not found")
        raise ValueError("invalid format")

