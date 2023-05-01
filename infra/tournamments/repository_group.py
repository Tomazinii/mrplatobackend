from interfaces.repository import GroupRepositoryInterface
from .models import Group

from domain.entities.tournamment import Group as GroupEntitie


class GroupRepository(GroupRepositoryInterface):
    
    @classmethod
    def add(self, turma, name, slug):
        try:
            obj: Group = Group.objects.get_or_create(turma=turma, name=name, slug=slug)
            
            entitie = GroupEntitie.create(obj[0].turma.id, obj[0].name)
            return entitie
        except Exception as exc:
            raise Exception(exc)

        