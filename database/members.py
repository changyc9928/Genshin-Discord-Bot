import json
import os
import genshin
from genshin.client import GenshinClient


class ServerData:
    data = {}

    @staticmethod
    def register(uid: str):
        if uid not in ServerData.data:
            ServerData.data[uid] = Account(uid)
            ServerData.save_json()
            return True
        return False

    @staticmethod
    def set_cookies(uid: str, ltoken, ltuid):
        if uid not in ServerData.data:
            return False
        ServerData.data[uid].set_cookies(ltoken, ltuid)
        ServerData.save_json()
        return True

    @staticmethod
    def delete(uid: str):
        if uid not in ServerData.data:
            return False
        del ServerData.data[uid]
        ServerData.save_json()
        return True

    @staticmethod
    def set_authkey(uid: str, url) -> bool:
        if uid not in ServerData.data:
            return False
        ServerData.data[uid].set_authkey(url)
        ServerData.save_json()
        return True

    @staticmethod
    def get_client(uid: str):
        # print(id)
        # print(ServerData.data[uid])
        if uid not in ServerData.data:
            return
        return GenshinClient(ServerData.data[uid].cookies, genshin.extract_authkey(ServerData.data[uid].authkey))

    @staticmethod
    def get_authkey(uid: str):
        if uid not in ServerData.data:
            return
        return genshin.extract_authkey(ServerData.data[uid].authkey)
        # if uid not in member.accounts:
        #     return
        # return member.accounts[uid].authkey

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
        for uid, data in data_.items():
            new_user = Account(data["uid"])
            new_user.set_cookies(data['cookies']['ltoken'], data['cookies']['ltuid'])
            # for _, acc in data['accounts'].items():
            #     new_user.add_account(acc["uid"])
            new_user.set_authkey(data["authkey"])
            ServerData.data[uid] = new_user
        # print(json.dumps(ServerData.data, default=lambda o: o.__dict__, indent=4))


# class Member:
#     def __init__(self, name) -> None:
#         self.name = name
#         self.cookies = {"ltuid": 0,
#                         "ltoken": ""}
#         self.accounts = {}

#     def add_account(self, uid):
#         self.accounts[uid] = Account(uid)

#     def set_cookies(self, ltoken, ltuid):
#         self.cookies["ltoken"] = ltoken
#         self.cookies["ltuid"] = ltuid

#     def set_authkey(self, uid, url) -> bool:
#         if uid not in self.accounts:
#             return False
#         self.accounts[uid].set_authkey(genshin.extract_authkey(url))
#         return True


class Account:
    def __init__(self, uid) -> None:
        self.uid = uid
        self.cookies = {"ltuid": 0,
                        "ltoken": ""}
        self.authkey = None

    def set_authkey(self, authkey):
        self.authkey = authkey

    def set_cookies(self, ltoken, ltuid):
        self.cookies["ltoken"] = ltoken
        self.cookies["ltuid"] = ltuid