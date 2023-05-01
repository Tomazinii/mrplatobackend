#improvisado

from interfaces.repository.user_repository import UserRepository as UserRepositoryInterface

from infra.user.models import UserAccount
from domain.entities.user import User

class UserRepository(UserRepositoryInterface):

    @classmethod
    def add_register_students(file, Class):
        """ add register User Receipt

        Args:
            file (_type_): _description_
            Class (_type_): _description_
        """
        pass

    @classmethod
    def add(self, username, email, matriculation, password, turma=None):
        """ add User in database

        Args:
            username (_type_): _description_
            email (_type_): _description_
            matriculation (_type_): _description_
            password (_type_): _description_
            turma (_type_, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """

        try:
            user = UserAccount.objects.create_user(username=username, email=email, matriculation=matriculation,password=password,turma=turma[0])
            return user
        except:
            raise Exception("ERROR")
            
    def find_by_email(self, email) -> User:
        """ find user method

        Args:
            email (_type_): _description_

        Raises:
            Exception: _description_
        """
        
        try:
            if email:
                user = UserAccount.objects.filter(email=email)
                return user
        except:
            raise Exception("error")

    def find_by_id(self, id):
        try:
            user = UserAccount.objects.filter(id=id)
            return user
        except Exception as exc:
            raise Exception(exc)