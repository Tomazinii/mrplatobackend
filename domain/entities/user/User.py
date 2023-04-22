from domain.entities.objectValue import Email

class User:
    id: int
    username: str
    email: Email
    nick: str
    matriculation:str
    turma:int

    def __init__(self, username: str, id: int, turma: int, matriculation: str, nick: str, email: Email):
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
            return User(usermame, id, turma, matriculation, nick, email_obj)
        raise Exception("error")
        

