from typing import Type
from interfaces.gateways import GatewayUsecaseInterface
from interfaces.use_case import CreateGroupInterface

class CreateGroupGateway(GatewayUsecaseInterface):

    def __init__(self, usecase: Type[CreateGroupInterface]):
        self.usecase = usecase

    def execute(self, data):

        if data:
            turma = data["turma"]
            name = data["name"]
            response = self.usecase.create(name=name, turma=turma,)
            return response

        raise Exception("No found data")