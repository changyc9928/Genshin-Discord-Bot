import datetime
import json


class Coop:

    message_id = 0
    data = {}

    @staticmethod
    def convert_to_json():
        return json.dumps(Coop.data, default=lambda o: o.__dict__, indent=4)


class UserData:
    def __init__(self, name) -> None:
        self.name = name
        self.time = datetime.datetime.today().replace(hour=22, minute=30, second=0, microsecond=0).astimezone().strftime('%Y-%m-%d %H:%M %Z')
        self.weapon = []
        self.leyline = []
        self.talent = []
        self.world_boss = []
        self.trounce = []

        self.ltoken = 0
        self.luid = 0
        self.authkey = None