from scoring.abstract import AbstractScoring


class DefaultScoring(AbstractScoring):
    @property
    def higher_better(self):
        return True

    def validate(self, submission_text: str):
        return True, None

    def score(self, submission_text: str):
        return 2, 1, None
