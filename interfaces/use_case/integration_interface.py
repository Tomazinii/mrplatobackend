from abc import ABC,abstractmethod
from typing import Dict

class IntegrationInterface(ABC):

    @abstractmethod
    def apply(sel_lines: list, index_exercise: int, index_list_exercise: int, selected_rule_index: dict, new_line: list) -> dict:
        raise Exception("Method not implemented")
