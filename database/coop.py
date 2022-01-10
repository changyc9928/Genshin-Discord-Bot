import datetime
import json
import os.path


class Coop:

    message_id = 0
    data = {}

    @staticmethod
    def convert_to_json():
        return json.dumps(Coop.data, default=lambda o: o.__dict__, indent=4)

    @staticmethod
    def load_json():
        if not os.path.isfile("data.json"):
            return
        with open("data.json", "r") as file:
            data_ = json.loads(file.read())
        for user_id, data in data_.items():
            new_user = CoopData(data["name"])
            new_user.time = data["time"]
            new_user.weapon = data["weapon"]
            new_user.leyline = data["leyline"]
            new_user.artifact = data['artifact']
            new_user.talent = data["talent"]
            new_user.world_boss = data["world_boss"]
            new_user.trounce = data["trounce"]

            Coop.data[int(user_id)] = new_user

    @staticmethod
    def add_user(user):
        if user.id not in Coop.data:
            Coop.data[user.id] = CoopData(user.name)
            Coop.save_json()

    @staticmethod
    def delete_user(user):
        if user.id in Coop.data:
            del Coop.data[user.id]
            Coop.save_json()

    def save_json():
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(Coop.data, f, ensure_ascii=False,
                      indent=4, default=lambda o: o.__dict__)

    def reset_data():
        Coop.data = {}
        Coop.save_json()


class CoopData:
    def __init__(self, name) -> None:
        self.name = name
        self.time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(
            hour=22, minute=30, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M %Z')
        self.weapon = []
        self.leyline = []
        self.talent = []
        self.artifact = []
        self.world_boss = []
        self.trounce = []

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
        elif tag == "World Bosses":
            self.world_boss = []
            data = self.world_boss
        ret = ""
        for val in values:
            ret += f"You're attending {val}\n"
            data.append(val)
        if ret == "":
            ret = f"Paimon canceled all your bookings on {tag} today."
        Coop.save_json()
        return ret

    def change_time(self, msg):
        self.time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(
            hour=int(msg[:2]), minute=int(msg[2:]), second=0, microsecond=0)
        if 0 <= int(msg) <= 60:
            self.time += datetime.timedelta(days=1)
        self.time = self.time.strftime('%Y-%m-%d %H:%M %Z')
        Coop.save_json()
