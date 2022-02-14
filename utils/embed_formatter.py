from datetime import datetime

class EmbedFormatter():
    def __init__(self, data, embed):
        self.data = data
        self.embed = embed

    def format_attendance(self):
        return "".join([f"➡️ {self.data[key]['name']} at {self.data[key]['time']}\n" for key in self.data.keys()])
    
    def format_materials(self):
        ret = ""
        for key in self.data.keys():
            member = self.data[key]
            if member["attend"]:
                ret += f"**{member['name']} is farming:**\n"
                materials = ""
                if len(member['weapon']) > 0:
                    materials += self.format_materials_field("⚔️ Weapons", member['weapon'])
                if len(member['leyline']) > 0:
                    materials += self.format_materials_field("🌿 Leylines", member['leyline'])
                if len(member['talent']) > 0:
                    materials += self.format_materials_field("📚 Talents", member['talent'])
                if len(member['artifact']) > 0:
                    materials += self.format_materials_field("👑 Artifacts", member['artifact'])
                if len(member['world_boss']) > 0:
                    materials += self.format_materials_field("🌺 World Bosses", member['world_boss'])
                if len(member['trounce']) > 0:
                    materials += self.format_materials_field("🐸 Trounce", member['trounce'])
                if len(materials) == 0:
                    ret += "Haven't ordered anything yet 🤷"
                else:
                    ret += materials
                ret += "\n"
        return ret

    def format_materials_field(self, title, materials):
        return f"> {title} - {''.join([material + ', ' for material in materials])[:-2]}\n"

    def format_embed(self):
        self.embed.set_thumbnail(url="https://upload-os-bbs.hoyolab.com/upload/2021/07/13/69629320/6a559ac21593156204bfa72c6faaea3b_6954693156943762270.gif?x-oss-process=image/resize,s_500/quality,q_80/auto-orient,0/interlace,1/format,gif")
        self.embed.add_field(name="Who's ikuyo-ing?", value=self.format_attendance(), inline=False)
        self.embed.add_field(name="Farming menu orders for today", value=self.format_materials(), inline=False)
        self.embed.set_footer(text=f"Menu ordered and updated by Painmon at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", icon_url="https://64.media.tumblr.com/e2358326f171b07a12cc09f46adc8a4f/d900fba9b3ad6ca6-88/s400x600/2568b87b5ccf0c7f2440e54df642328b90d7e0f6.png")
