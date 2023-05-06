from urllib import response
from interfaces.routes import RouteInterface
from typing import Type
from controllers.helpers import HttpRequest, HttpResponse


def admin_adapter(request: any, api_route: Type[RouteInterface]):

    http_request = HttpRequest(header=request.headers, files=request.FILES, body=request.POST)

    try:
        response = api_route.route(http_request)
        return response
        
    except Exception as exc:
        return HttpResponse(400, body=str(exc))

