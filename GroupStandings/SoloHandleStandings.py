from objects.Contest import *
from objects.Problem import *
from objects.RanklistRow import *

class SoloHandleStandings:
    def __init__(self, contest : Contest, problems : list[Problem], problemResults : list[ProblemResult]):
        self.contest = contest
        self.problems = problems
        self.problemResults = problemResults
