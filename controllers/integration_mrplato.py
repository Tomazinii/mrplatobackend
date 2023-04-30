from importlib import import_module
from interfaces.routes import RouteInterface
from controllers.helpers import HttpRequest,HttpResponse
from interfaces.use_case import IntegrationInterface
from typing import Type
from controllers.errors.http_error import HttpErrors

class IntegrationController(RouteInterface):

    def __init__(self, usecase: Type[IntegrationInterface]):
        self.usecase = usecase
        self.http_error = HttpErrors()

    def route(self, request: Type[HttpRequest]) -> HttpResponse:

        if request.body:

            params = request.body.keys()
            print("OKOKOKO",params)


            if "sel_lines" in params and "index_exercise" in params and  "index_list_exercise" in params and "selected_rule_index" in params and "list_new_line" in params:
                sel_lines = request.body["sel_lines"]
                index_exercise = request.body["index_exercise"]
                index_list_exercise = request.body["index_list_exercise"]
                selected_rule_index = request.body["selected_rule_index"]
                list_new_line = request.body["list_new_line"]
                response = self.usecase.apply(sel_lines=sel_lines, index_exercise=index_exercise,index_list_exercise=index_list_exercise, selected_rule_index=selected_rule_index, new_line=list_new_line)

                return HttpResponse(201, response)
            else:
                return HttpResponse(self.http_error.error_422()["status_code"],  self.http_error.error_422()["body"])
            
        else:
            return HttpResponse(self.http_error.error_400()["status_code"], self.http_error.error_400()["body"])

