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

    def __add__(self, other):
        if other is None:
            return self
        if isinstance(other, ProblemResult):
            if self.points > 0:
                # Problem already solved; no need to merge any otther results
                return self

            # Problem did not solved; needs to "merge" other to self
            return ProblemResult({
                "points": other.points,
                "penalty": sum(
                    filter(
                        lambda x : x is not None,
                        [self.penalty, other.penalty]
                    )
                ),
                "rejectedAttemptCount": self.rejectedAttemptCount + other.rejectedAttemptCount,
                "type": "MERGED",
                "bestSubmissionTimeSeconds": other.bestSubmissionTimeSeconds
            })
        return NotImplemented
