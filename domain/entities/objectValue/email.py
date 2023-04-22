import re


class Email:

    __email: str

    def __init__(self, email):
         self.__email = email

    @staticmethod
    def create(email: str):
        if Email.validate(email):
            return Email(email)
        return ValueError("invalid email")

    @staticmethod
    def validate(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not isinstance(email, str):
            return False
        
        if len(email) > 256:

            return False
    
        if re.match(email_regex, email):
            return True
        return False


    def get_email(self):
        return self.__email
        