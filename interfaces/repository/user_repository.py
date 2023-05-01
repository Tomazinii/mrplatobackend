


from abc import ABC, abstractmethod


class UserRepository(ABC):
    
    @abstractmethod
    def add_register_students(file, Class):
        raise Exception("method not implemented")
        

    @abstractmethod
    def add(self, username, email, matriculation, password, turma):
        raise Exception("method not implemented")
    
    @abstractmethod
    def find_by_email(self, email):
        raise Exception("method not implemented")
    
    @abstractmethod
    def find_by_id(self, id):
        raise Exception("method not implemented")
        