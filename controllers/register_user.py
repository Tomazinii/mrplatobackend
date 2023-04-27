from interfaces.routes import RouteInterface
from controllers.helpers import HttpRequest,HttpResponse
from interfaces.use_case import RegisterUserInterface
from typing import Type
from controllers.errors.http_error import HttpErrors

class RegisterController(RouteInterface):

    def __init__(self, usecase: Type[RegisterUserInterface]):
        self.usecase = usecase
        self.http_error = HttpErrors()


    def route(self, request: Type[HttpRequest]) -> HttpResponse:

        if request.files and request.body:
            params = request.files
            params_body = request.body


            if "archive" in params and "turma" in params_body:
                with request.files["archive"].open("r") as txt:
                    array = txt.readlines()
                array = [z.decode() for z in array]
                class_id = int(request.body["turma"])
                response = self.usecase.register_users(Class=class_id, file=array)
                return HttpResponse(201, response)
            else:
                return HttpResponse(self.http_error.error_422()["status_code"],  self.http_error.error_422()["body"])
        else:
            return HttpResponse(self.http_error.error_400()["status_code"], self.http_error.error_400()["body"])

