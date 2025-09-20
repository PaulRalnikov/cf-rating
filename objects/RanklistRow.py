from objects.Party import Party
from objects.ProblemResult import *

class RanklistRow:
    def __init__(self, params : dict):
        self.party = Party(params["party"])
        self.rank = params.get("rank")
        self.points = params.get("points")
        self.penalty = params.get("penalty")
        self.successfulHackCount = params.get("successfulHackCount")
        self.unsuccessfulHackCount = params.get("unsuccessfulHackCount")
        self.problemResults = list(map(ProblemResult, params.get("problemResults")))
        self.lastSubmissionTimeSeconds = params.get("lastSubmissionTimeSeconds")

    def __str__(self):
        return (f"Contestant(party='{self.party}', rank={self.rank}, points={self.points}, "
                f"penalty={self.penalty}, successfulHackCount={self.successfulHackCount}, "
                f"unsuccessfulHackCount={self.unsuccessfulHackCount}, problemResults={self.problemResults}, "
                f"lastSubmissionTimeSeconds={self.lastSubmissionTimeSeconds})")

    def __repr__(self):
        return self.__str__()

    def get_handle(self):
        if len(self.party.members) != 1:
            return None
        return self.party.members[0].handle
