from interfaces.use_case import FindUserInterface
from interfaces.repository import UserRepository
from domain.entities.objectValue import Email
from domain.entities.user import User


class FindUser(FindUserInterface):

    def __init__(self, repository: UserRepository):
        self.repository = repository


    def by_email(self, email: str) -> User:
        email = Email.create(email)

        if isinstance(email, Email):
            user = self.repository.find_by_email(email=email.get_email())
            return user
        
        raise Exception("Invalid email")

    def by_id(self, id: int) -> User:

        if isinstance(id, int):
            user = self.repository.find_by_id(id)
            return user
        
        raise Exception("Invalid type")
        
                
    
