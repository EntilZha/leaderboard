from abc import ABCMeta, abstractmethod
from typing import Tuple


class AbstractScoring(metaclass=ABCMeta):
    @property
    @abstractmethod
    def higher_better(self) -> bool:
        pass

    @abstractmethod
    def validate(self, submission_text: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def score(self, submission_text: str) -> Tuple[float, str]:
        pass

