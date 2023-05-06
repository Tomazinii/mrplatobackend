from controllers import CreateGroupController
from usecases import CreateGroup
from infra.tournamments.repository_group import GroupRepository
from infra.turma.repository import ClassRepository
from usecases import FindClass
from gateways.websocket import CreateGroupGateway

def create_group_composite():
    repository = GroupRepository()
    repository_support = ClassRepository()
    usecase_support = FindClass(repository=repository_support)
    usecase = CreateGroup(repository=repository, use_case_support=usecase_support)
    controller = CreateGroupController(usecase=usecase)
    return controller

def create_group_websocker_composite():
    repository = GroupRepository()
    repository_support = ClassRepository()
    usecase_support = FindClass(repository=repository_support)
    usecase = CreateGroup(repository=repository, use_case_support=usecase_support)
    gateway = CreateGroupGateway(usecase=usecase)
    return gateway