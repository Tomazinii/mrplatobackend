from abc import ABC, abstractmethod
from typing import Type

class RouteInterface(ABC):

    @abstractmethod
    def route(request):
        raise Exception("method not implemented")
