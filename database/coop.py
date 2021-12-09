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

    def book(self, tag, values):
        if tag == "Ley Line Outcrops":
            self.leyline = []
            data = self.leyline
        elif tag == "Weapon Ascension Materials":
            self.weapon = []
            data = self.weapon
        elif tag == "Talent Books":
            self.talent = []
            data = self.talent
        elif tag == "Artifacts":
            self.artifact = []
            data = self.artifact
        elif tag == "Trounce Domains":
            self.trounce = []
            data = self.trounce
        elif tag == "World Boss":
            self.world_boss = []
            data = self.world_boss
        ret = ""
        for val in values:
            ret += f"You're attending {val}\n"
            data.append(val)
        return ret

    def change_time(self, msg):
        self.time = datetime.datetime.today().replace(hour=int(msg[:2]), minute=int(msg[2:]), second=0, microsecond=0).astimezone()
        if 0 <= int(msg) <= 60:
            self.time += datetime.timedelta(days=1)
        self.time = self.time.strftime('%Y-%m-%d %H:%M %Z')