from typing import Type
from interfaces.routes import RouteInterface
from interfaces.use_case import CreateGroupInterface
from controllers.helpers import HttpRequest,HttpResponse
from controllers.errors import HttpErrors


class CreateGroupController(RouteInterface):

    def __init__(self, usecase: Type[CreateGroupInterface]):
        self.usecase = usecase
        self.htt_erro = HttpErrors()

    def route(self, request: HttpRequest) -> HttpResponse:
        
        if request.body:
            params = request.body.keys()

            if "turma" in params and "name" in params:
                turma = request.body["turma"]
                name = request.body["name"]
                response = self.usecase.create(turma=turma, name=name)

                return HttpResponse(201, response)
            
            return HttpResponse(self.htt_erro.error_422()["status_code"],self.htt_erro.error_422()["body"])
        
        return HttpResponse(self.htt_erro.error_400()["status_code"],self.htt_erro.error_400()["body"])
        