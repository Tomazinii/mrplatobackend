from interfaces.routes import RouteInterface
from interfaces.use_case import GetListExerciseInterface
from typing import Type
from controllers.helpers import HttpRequest, HttpResponse
from controllers.errors import HttpErrors

class GetListExerciseController(RouteInterface):

    def __init__(self, usecase: Type[GetListExerciseInterface]):
        self.usecase = usecase


    def route(self, request: Type[HttpRequest]) -> HttpResponse:
        response = None

        if request.query:
            keys = request.query.keys()

            if "index_list_exercise" in keys:
                index_list_exercise = request.query["index_list_exercise"]
                response = self.usecase.get_list(index_list_exercise=index_list_exercise)
                return HttpResponse(200, response)
            
            else:
                http_error = HttpErrors()
                return HttpResponse(http_error.error_422()["status_code"], http_error.error_422()["body"])

        else:
            response = self.usecase.get_list()
            return HttpResponse(200, response)

        