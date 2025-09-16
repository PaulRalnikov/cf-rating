import logging
logger = logging.getLogger(__name__)

class Contest:
    # used to unitialize from cf api respone
    def __init__(self, params : dict):
        self.id = params["id"]
        self.name = params["name"]
        self.type = params["type"]
        self.phase = params["phase"]
        self.frozen = params["frozen"]
        self.durationSeconds = params["durationSeconds"]
        self.startTimeSeconds = params["startTimeSeconds"]
        self.relativeTimeSeconds = params["relativeTimeSeconds"]
        self.preparedBy = params["preparedBy"]

    def __str__(self):
        return (f"Contest(id={self.id}, name='{self.name}', type='{self.type}', phase='{self.phase}', "
                f"frozen={self.frozen}, durationSeconds={self.durationSeconds}, "
                f"startTimeSeconds={self.startTimeSeconds}, relativeTimeSeconds={self.relativeTimeSeconds}, "
                f"preparedBy='{self.preparedBy}')")

    def __repr__(self):
        return self.__str__()
