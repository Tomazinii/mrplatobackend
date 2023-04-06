from interfaces.routes import RouteInterface
from typing import Type
from controllers.helpers import HttpRequest,HttpResponse
from controllers.errors import HttpErrors

http_error = HttpErrors()

def django_adapter(request: any, api_route: Type[RouteInterface]):
    query_string = request.query_params
    http_request = HttpRequest(header=request.headers,body=request.data, query=query_string)
    try:
        response = api_route.route(http_request)
        return response
    except Exception as exc:
        return HttpResponse(400, body=str(exc))