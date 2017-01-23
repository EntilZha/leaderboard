from abc import ABCMeta, abstractmethod
from typing import Tuple, Union
import importlib


class AbstractScoring(metaclass=ABCMeta):
    @property
    @abstractmethod
    def higher_better(self) -> bool:
        pass

    @abstractmethod
    def validate(self, submission_text: str) -> Tuple[bool, Union[str, None]]:
        pass

    @abstractmethod
    def score(self, submission_text: str) -> Tuple[float, float, Union[str, None]]:
        pass


def get_class(instance_module_class: str):
    instance_module, instance_class = instance_module_class.rsplit('.')
    py_instance_module = importlib.import_module(instance_module)
    py_instance_class = getattr(py_instance_module, instance_class)
    return py_instance_class
