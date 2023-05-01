

from typing import Type
from interfaces.use_case import RegisterMemberInterface, FindUserInterface, FindGroupInterface
from interfaces.repository import MemberRepositoryInterface
from domain.entities.tournamment import Member

class RegisterMember(RegisterMemberInterface):

    def __init__(self, reposistory: Type[MemberRepositoryInterface], usecase_find_user: Type[FindUserInterface], usecase_find_group: Type[FindGroupInterface]):
        self.repository = reposistory
        self.usecase_find_user = usecase_find_user
        self.usecase_find_group = usecase_find_group
    
    def register(self, user, group, online=False, boss=False) -> Member:
        find_user = self.usecase_find_user.by_id(user)
        find_group = self.usecase_find_group.find(group)
        if find_user:
            registered_member_verification = self.repository.find_user(find_user[0])

            if not registered_member_verification:
                if find_group:
                    result = self.repository.register(user=find_user, group=find_group, online=online, boss=boss)
                    return result
                raise Exception("Group not found")
            raise Exception("User already belongs to a group")
        raise Exception("User not found")

