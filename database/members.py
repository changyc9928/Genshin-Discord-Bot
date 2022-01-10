import json
import os
import genshin
from genshin.client import GenshinClient


class ServerData:
    data = {}

    @staticmethod
    def register(id, name):
        if id not in ServerData.data:
            ServerData.data[id] = Member(name)
            ServerData.save_json()
            return True
        return False

    @staticmethod
    def set_cookies(id, ltoken, ltuid):
        if id not in ServerData.data:
            return False
        ServerData.data[id].set_cookies(ltoken, ltuid)
        ServerData.save_json()
        return True

    @staticmethod
    def register_account(id, uid):
        if id not in ServerData.data:
            return False
        ServerData.data[id].add_account(uid)
        ServerData.save_json()
        return True

    @staticmethod
    def set_authkey(id, uid, url) -> bool:
        if id not in ServerData.data:
            return False
        ret = ServerData.data[id].set_authkey(uid, url)
        ServerData.save_json()
        return ret

    @staticmethod
    def get_client(id):
        # print(id)
        if id not in ServerData.data:
            return
        return GenshinClient(ServerData.data[id].cookies)

    @staticmethod
    def get_authkey(id, uid):
        if id not in ServerData.data:
            return
        member = ServerData.data[id]
        if uid not in member.accounts:
            return
        return member.accounts[uid].authkey

    def save_json():
        with open('member.json', 'w', encoding='utf-8') as f:
            json.dump(ServerData.data, f, ensure_ascii=False,
                      indent=4, default=lambda o: o.__dict__)

    @staticmethod
    def load_json():
        if not os.path.isfile("member.json"):
            return
        with open("member.json", "r") as file:
            data_ = json.loads(file.read())
        for user_id, data in data_.items():
            new_user = Member(data["name"])
            new_user.set_cookies(data['cookies']['ltoken'], data['cookies']['ltuid'])
            for _, acc in data['accounts'].items():
                new_user.add_account(acc["uid"])
                new_user.accounts[acc["uid"]].authkey = acc["authkey"]
            ServerData.data[int(user_id)] = new_user
        # print(json.dumps(ServerData.data, default=lambda o: o.__dict__, indent=4))


class Member:
    def __init__(self, name) -> None:
        self.name = name
        self.cookies = {"ltuid": 0,
                        "ltoken": ""}
        self.accounts = {}

    def add_account(self, uid):
        self.accounts[uid] = Account(uid)

    def set_cookies(self, ltoken, ltuid):
        self.cookies["ltoken"] = ltoken
        self.cookies["ltuid"] = ltuid

    def set_authkey(self, uid, url) -> bool:
        if uid not in self.accounts:
            return False
        self.accounts[uid].set_authkey(genshin.extract_authkey(url))
        return True


class Account:
    def __init__(self, uid) -> None:
        self.uid = uid
        self.authkey = None

    def set_authkey(self, authkey):
        self.authkey = authkey
