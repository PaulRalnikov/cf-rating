
class Member:
    def __init__(self, params : dict):
        self.handle = params.get("handle")
        self.name = params.get("name")

    def __str__(self):
        return f"Member(handle={self.handle}, name={self.name})"

    def __repr__(self):
        return self.__str__()
