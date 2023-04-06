from abc import ABC, abstractmethod
from typing import Type
from controllers.helpers import HttpResponse, HttpRequest

class RouteInterface(ABC):

    @abstractmethod
    def route(request: Type[HttpRequest]) -> HttpResponse:
        raise Exception("method not implemented")
