from interfaces.repository import MemberRepositoryInterface
from domain.entities.tournamment import Member
from .models import Members

class MemberRepository(MemberRepositoryInterface):

    @classmethod
    def register(self, user, group, online, boss) -> Member:
        try:
            member = Members.objects.get_or_create(user=user[0], group=group[0], online=online, boss=boss)
            return member
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod    
    def find_user(self, user) -> bool:
        member = Members.objects.filter(user=user)
        if member:
            return True
        return False
