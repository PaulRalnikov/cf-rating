from objects.cf.Member import *

class Party:
    def __init__(self, params : dict):
        self.contestId = params.get("contestId")
        self.members = list(map(Member, params.get("members")))
        self.participantType = params.get("participantType")
        self.teamId = params.get("teamId")
        self.teamName = params.get("teamName")
        self.ghost = params.get("ghost")
        self.room = params.get("room")
        self.startTimeSeconds = params.get("startTimeSeconds")

    def __str__(self):
        return (f"Party(contestId={self.contestId}, members={self.members}, participantType='{self.participantType}', "
                f"teamId={self.teamId}, teamName='{self.teamName}', ghost={self.ghost}, room={self.room}, "
                f"startTimeSeconds={self.startTimeSeconds})")

    def __repr__(self):
        return self.__str__()
