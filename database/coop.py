import datetime


class Coop:

    message_id = 0
    data = {}


class UserData:
    def __init__(self, name) -> None:
        self.name = name
        self.time = datetime.datetime.today()
        self.weapon = []
        self.leyline = []
        self.talent = []
        self.world_boss = []
        self.trounce = []

        self.ltoken = 0
        self.luid = 0
        self.authkey = None