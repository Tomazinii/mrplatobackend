from typing import Type
from interfaces.gateways import GatewayUsecaseInterface


def websocket_adapter(data: any, gateway: Type[GatewayUsecaseInterface]):
    try:
        response = gateway.execute(data)
        return response

    except:
        raise Exception("Error")
