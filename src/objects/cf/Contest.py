import logging
logger = logging.getLogger(__name__)

class Contest:
    # used to unitialize from cf api respone
    def __init__(self, params : dict):
        self.id = params.get("id")
        self.name = params.get("name")
        self.type = params.get("type")
        self.phase = params.get("phase")
        self.frozen = params.get("frozen")
        self.durationSeconds = params.get("durationSeconds")
        self.startTimeSeconds = params.get("startTimeSeconds")
        self.relativeTimeSeconds = params.get("relativeTimeSeconds")
        self.preparedBy = params.get("preparedBy")

    def __str__(self):
        return (f"Contest(id={self.id}, name='{self.name}', type='{self.type}', phase='{self.phase}', "
                f"frozen={self.frozen}, durationSeconds={self.durationSeconds}, "
                f"startTimeSeconds={self.startTimeSeconds}, relativeTimeSeconds={self.relativeTimeSeconds}, "
                f"preparedBy='{self.preparedBy}')")

    def __repr__(self):
        return self.__str__()
