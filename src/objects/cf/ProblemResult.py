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
            def choose_best_time(time_1 : int | None, time_2 : int | None):
                if time_1 is None:
                    return time_2
                if time_2 is None:
                    return time_1
                return min(time_1, time_2)

            return ProblemResult({
                "points": self.points + other.points,
                "penalty": sum(
                    filter(
                        lambda x : x is not None,
                        [self.penalty, other.penalty]
                    )
                ),
                "rejectedAttemptCount": self.rejectedAttemptCount + other.rejectedAttemptCount,
                "type": "MERGED",
                "bestSubmissionTimeSeconds": choose_best_time(self.bestSubmissionTimeSeconds, other.bestSubmissionTimeSeconds)
            })
        return NotImplemented
