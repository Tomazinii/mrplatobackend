from interfaces.routes import RouteInterface
from interfaces.use_case import RegisterListExerciseInterface
from typing import Type
from controllers.helpers import HttpRequest, HttpResponse
from controllers.errors import HttpErrors

class RegisterListExerciseController(RouteInterface):
    
    def __init__(self, usecase: Type[RegisterListExerciseInterface]):
        self.usecase = usecase
        self.http_error = HttpErrors()

    def route(self, request: HttpRequest):
        
        if request.files and request.body:
            params = request.files
            params_body = request.body

            if "file" in params and "list_name" in params_body:
                file = request.files["file"]
                list_name = request.body["list_name"]
                array = file.readlines()
                array = [z.decode("utf-8") for z in array]

                response = self.usecase.register(array, list_name)
                
                return HttpResponse(201, response)
            
            else:
                return HttpResponse(self.http_error.error_422()["status_code"],  self.http_error.error_422()["body"])
        else:
            return HttpResponse(self.http_error.error_400()["status_code"], self.http_error.error_400()["body"])




