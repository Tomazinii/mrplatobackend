from interfaces.use_case import RegisterUserInterface
from interfaces.repository import UserRepository
from typing import Type, List
from domain.entities.user import User
from domain.entities.user import RegisterUser as RegisterUserEntitie
from interfaces.use_case import FindClassInterface, FindUserInterface


class RegisterUser(RegisterUserInterface):

    def __init__(self, repository: Type[UserRepository], find_class_use_case: FindClassInterface, find_user_use_case:FindUserInterface,  notication="notification_service" ):
        self.repository = repository
        self.find_class = find_class_use_case
        self.find_user = find_user_use_case

    def register_users(self, file, Class) -> List[User]:

        data: RegisterUserEntitie = RegisterUserEntitie.create(file, Class)
        
        if isinstance(data, RegisterUserEntitie):
           return self.add_user(data)
        
        raise Exception("Error create user")
        

    
    def add_user(self, data: RegisterUserEntitie):
        user_list = data.get_data()
        
        result_list = []

        if self.find_class.find(data.Class):
            turma = self.find_class.find(data.Class)
            for line in user_list:
                if not self.find_user.by_email(line["email"]):

                    result = self.repository.add(username=line["username"], email=line["email"], matriculation=line["matriculation"], password=line["matriculation"], turma=turma)
                    result_list.append(result)

        return result_list
