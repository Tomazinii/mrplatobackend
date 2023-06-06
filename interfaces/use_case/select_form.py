from abc import ABC, abstractmethod


class SelectFormInterface(ABC):

    @abstractmethod
    def apply(sel_rule: int, sel_lines: int, index_exercise: int, index_list_exercise: int, new_line: list, option_index:int):
        raise Exception("method not implemented")