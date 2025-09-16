class RanklistRow:
    def __init__(self, params : dict):
        self.party = params["party"]
        self.rank = params["rank"]
        self.points = params["points"]
        self.penalty = params["penalty"]
        self.successfulHackCount = params["successfulHackCount"]
        self.unsuccessfulHackCount = params["unsuccessfulHackCount"]
        self.problemResults = params["problemResults"]
        self.lastSubmissionTimeSeconds = None if "lastSubmissionTimeSeconds" not in params else params["lastSubmissionTimeSeconds"]

    def __str__(self):
        return (f"Contestant(party='{self.party}', rank={self.rank}, points={self.points}, "
                f"penalty={self.penalty}, successfulHackCount={self.successfulHackCount}, "
                f"unsuccessfulHackCount={self.unsuccessfulHackCount}, problemResults={self.problemResults}, "
                f"lastSubmissionTimeSeconds={self.lastSubmissionTimeSeconds})")

    def __repr__(self):
        return self.__str__()
