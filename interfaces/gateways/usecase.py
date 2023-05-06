

from abc import ABC, abstractmethod


class GatewayUsecaseInterface(ABC):
    @abstractmethod
    def execute(data):
        raise Exception("method not imeplemented")