from objects.Contest import *


class Standings:
    def __init__(self, params : dict) :
        self.contest = Contest(params["contest"])
        self.problems = params["problems"]
        self.rows = params["rows"]

    def __str__(self):
        return f"Standings(contest id {self.contest.id}, problems : {self.problems}, rows : {self.rows})"

    def __repr__(self):
        return self.__str__()
