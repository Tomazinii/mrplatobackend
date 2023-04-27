from domain.entities.objectValue import Email

class User:
    id: int
    username: str
    email: Email
    nick: str
    matriculation:str
    turma:int

    def __init__(self, username: str, turma: int, matriculation: str, email: Email, nick: str = None, id: int = None):
        self.id = id
        self.username = username
        self.email = email
        self.matriculation = matriculation
        self.turma = turma
        self.nick = nick


    @staticmethod
    def create(id, usermame, email, nick, matriculation, turma):
        email_obj = Email.create(email)
        if isinstance(email_obj, Email):
            return User(usermame, turma, matriculation, email_obj, nick, id)
        raise Exception("error")
        

