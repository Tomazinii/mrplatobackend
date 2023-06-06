from typing import Type
from interfaces.routes import RouteInterface
from interfaces.use_case import SelectFormInterface
from controllers.helpers import HttpRequest, HttpResponse
from controllers.errors import HttpErrors

class SelectFormController(RouteInterface):

    def __init__(self, usecase: Type[SelectFormInterface]):
        self.usecase = usecase
        self.http_error = HttpErrors()

    def route(self, request: HttpRequest) -> HttpResponse:
        
        if request.body:
            request_params = request.body.keys()

            if "sel_rule" in request_params and "sel_lines" in request_params and "index_exercise" in request_params and "index_list_exercise" in request_params and "list_new_line" in request_params and "option_index" in request_params:
                sel_rule = request.body["sel_rule"]
                sel_lines = request.body["sel_lines"]
                index_exercise = request.body["index_exercise"]
                index_list_exercise = request.body["index_list_exercise"]
                option_index = request.body["option_index"]
                new_line = request.body["list_new_line"]
                response = self.usecase.apply(sel_rule=sel_rule, sel_lines=sel_lines, index_exercise=index_exercise,index_list_exercise=index_list_exercise,new_line=new_line,option_index=option_index)
                return HttpResponse(201, response)
            
            return HttpResponse(self.http_error.error_422()["status_code"], self.http_error.error_422()["body"])
        
        return HttpResponse(self.http_error.error_400()["status_code"], self.http_error.error_400()["body"])