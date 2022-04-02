from datetime import datetime
from datetime import timezone
from datetime import timedelta
from dateutil import parser
import random


class EmbedFormatter():
    def __init__(self, data, embed):
        self.data = data
        self.embed = embed
        self.count = 0

    def format_attendance(self):
        if len(self.data) == 0:
            return "> 🤷 Haven't recorded attendance yet"

        ret = ""
        for key in self.data.keys():
            if self.data[key]['attend']:
                ret += f"✅ {self.data[key]['name']}"
                if self.data[key]['time']:
                    ret += f" at {parser.parse(self.data[key]['time']).strftime('%I:%M %p')}\n"
                else:
                    ret += "\n"
            else:
                ret += f"🚫 {self.data[key]['name']} no ikuyo today\n"
        return ret

    def format_materials(self):
        ret = ""
        if len(self.data) == 0:
            return "> 🤷 Haven't ordered anything yet\n"
        order = 0
        for key in self.data.keys():
            member = self.data[key]
            if member["attend"]:
                ret += f"**{member['name']} is farming:**\n"
                materials = ""
                if len(member['weapon']) > 0:
                    materials += self.format_materials_field(
                        "⚔️ Weapons", member['weapon'])
                if len(member['leyline']) > 0:
                    materials += self.format_materials_field(
                        "🌿 Leylines", member['leyline'])
                if len(member['talent']) > 0:
                    materials += self.format_materials_field(
                        "📚 Talents", member['talent'])
                if len(member['artifact']) > 0:
                    materials += self.format_materials_field(
                        "👑 Artifacts", member['artifact'])
                if len(member['world_boss']) > 0:
                    materials += self.format_materials_field(
                        "🌺 World Bosses", member['world_boss'])
                if len(member['trounce']) > 0:
                    materials += self.format_materials_field(
                        "🐸 Trounce", member['trounce'])
                if len(materials) == 0:
                    ret += "> 🤷 Haven't ordered anything yet\n"
                    continue
                else:
                    # materials = f"> {chr(order + 97)} - {materials}"
                    ret += materials
                    self.count = 0

        
        # discord doesn't allow empty strings or else 400 bad request error :/
        if len(ret) == 0:
            return "> 🤷 Haven't ordered anything yet"
        print(ret)
        return ret

    def format_materials_field(self, title, materials):
        ret = f"> {title}:\n"
        for material in materials:
            ret += f"> \u0009{chr(self.count + 97)}. {material}\n"
            self.count += 1
        return ret
        # return f"{title} - {''.join([material + ', ' for material in materials])[:-2]}\n"

    def random_host(self):
        earliest_time = datetime(
            3000, 1, 1, tzinfo=timezone(timedelta(hours=8)))
        latest_time = datetime(1, 1, 1, tzinfo=timezone(timedelta(hours=8)))
        for _, val in self.data.items():
            if val["time"]:
                if parser.parse(val["time"]) < earliest_time:
                    earliest_time = parser.parse(val["time"])
                if parser.parse(val["time"]) > latest_time:
                    latest_time = parser.parse(val["time"])
        valid_host = []
        for _, val in self.data.items():
            if val["time"]:
                if parser.parse(val["time"]) == earliest_time:
                    valid_host.append(val["name"])
        if len(valid_host) > 0:
            i = random.randrange(0, len(valid_host))
            host = valid_host[i]
            return f"👻 {host} will be our host today online at {latest_time.strftime('%I:%M %p')}"
        return f"👻 Nobody is online today"

    def format_embed(self):
        self.embed.set_thumbnail(
            url="https://upload-os-bbs.hoyolab.com/upload/2021/07/13/69629320/6a559ac21593156204bfa72c6faaea3b_6954693156943762270.gif?x-oss-process=image/resize,s_500/quality,q_80/auto-orient,0/interlace,1/format,gif")
        self.embed.add_field(
            name="Host", value=self.random_host(), inline=False)
        self.embed.add_field(name="Who's ikuyo-ing?",
                             value=self.format_attendance(), inline=False)
        self.embed.add_field(name="Farming menu orders for today",
                             value=self.format_materials(), inline=False)
        self.embed.set_footer(text=f"Menu ordered and updated by Painmon at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                              icon_url="https://64.media.tumblr.com/e2358326f171b07a12cc09f46adc8a4f/d900fba9b3ad6ca6-88/s400x600/2568b87b5ccf0c7f2440e54df642328b90d7e0f6.png")
