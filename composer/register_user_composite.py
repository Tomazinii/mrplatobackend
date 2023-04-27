from controllers import RegisterController
from usecases.register_user import RegisterUser
from usecases import FindClass
from infra.turma.repository import ClassRepository
from infra.user.repository import UserRepository
from usecases import FindUser


def register_user_composer():
    repository = UserRepository()
    repository_find_class = ClassRepository()
    find_class_use_case = FindClass(repository_find_class)
    find_user_use_case = FindUser(repository)
    usecase = RegisterUser(repository=repository,find_class_use_case=find_class_use_case, find_user_use_case=find_user_use_case)
    controller = RegisterController(usecase=usecase)
    return controller