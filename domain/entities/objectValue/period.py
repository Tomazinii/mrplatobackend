
from datetime import date as dateType

class Period:
    __start: dateType
    __end: dateType

    def __init__(self, start: dateType, end: dateType) -> None:
        self.__start  = start
        self.__end = end

    def create_period(start: dateType, end: dateType):
        if isinstance(start, dateType) and isinstance(end, dateType):
            return Period(start, end)
        
        raise ValueError("invalid type")


    def get_period(self):
        return {"start": self.__start, "end": self.__end}