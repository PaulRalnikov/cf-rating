
class Problem:
    def __init__(self, params : dict):
        self.contestId = params["contestId"]
        self.problemsetName = None if "problemsetName" not in params else params["problemsetName"]
        self.index = params["index"]
        self.name = params["name"]
        self.name = params["name"]
        self.type = params["type"]
        self.type = params["type"]
        self.rating = params["rating"]
        self.tags = params["tags"]

    def __str__(self):
        return (f"Problem(contestId={self.contestId}, problemsetName='{self.problemsetName}', "
                f"index='{self.index}', name='{self.name}', type='{self.type}', "
                f"rating={self.rating}, tags={self.tags})")

    def __repr__(self):
        return self.__str__()
