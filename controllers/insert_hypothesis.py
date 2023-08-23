from interfaces.routes import RouteInterface
from controllers.helpers import HttpRequest,HttpResponse
from interfaces.use_case import InsertHypothesisInterface
from typing import Type
from controllers.errors.http_error import HttpErrors

class InsertionHypothesisController(RouteInterface):

    def __init__(self, usecase: Type[InsertHypothesisInterface]):
        self.usecase = usecase
        self.http_error = HttpErrors()

    def route(self, request: Type[HttpRequest]) -> HttpResponse:

        if request.body:
            params = request.body.keys()
 
            if "list_form" in params:
                list_form = request.body["list_form"]
                response = self.usecase.insert(list_form=list_form)
                return HttpResponse(201, response)
            else:
                return HttpResponse(self.http_error.error_422()["status_code"],  self.http_error.error_422()["body"])
            
        else:
            return HttpResponse(self.http_error.error_400()["status_code"], self.http_error.error_400()["body"])

