

from typing import Type
from interfaces.routes import RouteInterface
from interfaces.use_case import RegisterMemberInterface
from controllers.helpers import HttpRequest, HttpResponse
from controllers.errors import HttpErrors

class RegisterMemberController(RouteInterface):
    
    def __init__(self, usecase: Type[RegisterMemberInterface]):
        self.usecase = usecase
        self.http_error = HttpErrors()

    def route(self, request: HttpRequest) -> HttpResponse:

        if request.body:
            request_params = request.body.keys()
            if "user" in request_params and "group" in request_params:
                user = request.body["user"]
                group = request.body["group"]
                response = self.usecase.register(user=user, group=group)
                return HttpResponse(201, response)
            return HttpResponse(self.http_error.error_422()["status_code"], self.http_error.error_422()["body"])
        
        return HttpResponse(self.http_error.error_400()["status_code"], self.http_error.error_400()["body"])
        