from objects.cf.Contest import *
from objects.cf.Problem import *
from objects.cf.RanklistRow import *

class SoloHandleStandings:
    def __init__(self, contest : Contest, problems : list[Problem], problemResults : list[ProblemResult]):
        self.contest = contest
        self.problems = problems
        self.problemResults = problemResults
