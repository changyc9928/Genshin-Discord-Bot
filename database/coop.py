import datetime
import json


class Coop:

    message_id = 0
    data = {}

    @staticmethod
    def convert_to_json():
        return json.dumps(Coop.data, default=lambda o: o.__dict__, indent=4)

    @staticmethod
    def load_json():
        with open("data.json", "r") as file:
            data_ = json.loads(file.read())
        for user_id, data in data_.items():
            new_user = UserData(data["name"])
            new_user.time = data["time"]
            new_user.weapon = data["weapon"]
            new_user.leyline = data["leyline"]
            new_user.talent = data["talent"]
            new_user.world_boss = data["world_boss"]
            new_user.trounce = data["trounce"]

            new_user.ltoken = data["ltoken"]
            new_user.luid = data["luid"]
            new_user.authkey = data["authkey"]
            Coop.data[int(user_id)] = new_user

    @staticmethod
    def add_user(user):
        if user.id not in Coop.data:
            Coop.data[user.id] = UserData(user.name)
            Coop.save_json()
    
    @staticmethod
    def delete_user(user):
        if user.id in Coop.data:
            del Coop.data[user.id]
            Coop.save_json()

    def save_json():
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(Coop.data, f, ensure_ascii=False, indent=4, default=lambda o: o.__dict__)


class UserData:
    def __init__(self, name) -> None:
        self.name = name
        self.time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(hour=22, minute=30, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M %Z')
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
        Coop.save_json()
        return ret

    def change_time(self, msg):
        self.time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(hour=int(msg[:2]), minute=int(msg[2:]), second=0, microsecond=0)
        if 0 <= int(msg) <= 60:
            self.time += datetime.timedelta(days=1)
        self.time = self.time.strftime('%Y-%m-%d %H:%M %Z')
        Coop.save_json()