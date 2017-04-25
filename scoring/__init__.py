from scoring.abstract import AbstractScoring
from scoring.appthis import *

class DefaultScoring(AbstractScoring):
    @property
    def higher_better(self):
        return True

    def validate(self, submission_text: str):
        return True, None

    def score(self, submission_text: str):
        return 0, 0, None
