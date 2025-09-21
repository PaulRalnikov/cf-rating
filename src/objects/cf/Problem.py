
class Problem:
    def __init__(self, params : dict):
        self.contestId = params.get("contestId")
        self.problemsetName = params.get("problemsetName")
        self.index = params.get("index")
        self.name = params.get("name")
        self.type = params.get("type")
        self.points = params.get("points")
        self.rating = params.get("rating")
        self.tags = params.get("tags")

    def __str__(self):
        return (f"Problem(contestId={self.contestId}, problemsetName='{self.problemsetName}', "
                f"index='{self.index}', name='{self.name}', type='{self.type}', "
                f"rating={self.rating}, tags={self.tags})")

    def __repr__(self):
        return self.__str__()
