
from datetime import date as dateType

class Period:
    __start: dateType
    __end: dateType

    def __init__(self, start: dateType, end: dateType) -> None:
        self.__start  = start
        self.__end = end

    @staticmethod
    def validate(start: dateType, end: dateType) -> bool:
        if start.year >= start.today().year and start.month >= 1 and start.month <= 12:
            if end.year >= end.today().year and end.month >= 1 and end.month <= 12:
                 return True
            return False
        return False
        
    @staticmethod
    def create_period(start: dateType, end: dateType):
        if isinstance(start, dateType) and isinstance(end, dateType):
            if(Period.validate(start, end)):
                return Period(start, end)
            return ValueError("Invalid Object")
        raise ValueError("invalid type")


    def get_period(self):
        return {"start": self.__start, "end": self.__end}