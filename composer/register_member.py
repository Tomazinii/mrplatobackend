from controllers import RegisterMemberController
from infra.tournamments.repository_member import MemberRepository
from infra.user.repository import UserRepository
from infra.tournamments.repository_group import GroupRepository
from usecases import RegisterMember, FindGroup, FindUser


def register_member_composite():
    repository = MemberRepository()
    repository_user = UserRepository()
    repository_group = GroupRepository()
    usecase_find_user = FindUser(repository_user)
    usecase_find_group = FindGroup(repository_group)
    usecase = RegisterMember(reposistory=repository,usecase_find_group=usecase_find_group,usecase_find_user=usecase_find_user)
    controller = RegisterMemberController(usecase=usecase)
    return controller