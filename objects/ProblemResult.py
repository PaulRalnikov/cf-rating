class ProblemResult:
    def __init__(self, params : dict):
        self.points = params.get("points")
        self.penalty = params.get("penalty")
        self.rejectedAttemptCount = params.get("rejectedAttemptCount")
        self.type = params.get("type")
        self.bestSubmissionTimeSeconds = params.get("bestSubmissionTimeSeconds")

    def __str__(self):
        return (f"ProblemResult(points={self.points}, "
                f"penalty={self.penalty}, "
                f"rejectedAttemptCount={self.rejectedAttemptCount}, "
                f"type='{self.type}, "
                f"bestSubmissionTimeSeconds={self.bestSubmissionTimeSeconds})")

    def __repr__(self):
        return self.__str__()
