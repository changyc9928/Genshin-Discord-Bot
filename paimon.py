import discord
import genshin
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
import io
import aiohttp


domains = {
    0: "Mondsdalt Weapon",
    1: "Mondsdalt Talent",
    2: "Liyue Weapon",
    3: "Liyue Talent",
    4: "Inazuma Weapon",
    5: "Inazuma Talent",
    6: "Wolf",
    7: "Azhdaha",
    8: "Childe",
    9: "La Signora",
    "A": "Archaic Petra/Retracing Bolide",
    "B": "Thundering Fury/Thundersoother",
    "C": "Viridescent Venerer/Maiden Beloved",
    "D": "Crimson Witch of Flames/Lavawalker",
    "E": "Blizzard Strayer/Heart of Depth",
    "F": "Tenacity of the Millelith/Pale Flame",
    "G": "Shimenawa's Reminiscence/Emblem of Severed Fate",
    "H": "Husk of Opulent Dreams/Ocean-Hued Clam",
    "I": "Bloodstained Chivalry/Noblesse Oblige",
    "M": "Thunder Manifestation",
    "N": "Rhodeia of Loch",
    "O": "Pyro Regisvine",
    "P": "Pyro Hypostasis",
    "Q": "Primo Geovishap",
    "R": "Perpetual Mechanical Array", 
    "S": "Maguu Kenki",
    "T": "Hydro Hypostasis",
    "U": "Golden Wolflord",
    "V": "Geo Hypostasis",
    "W": "Electro Hypostasis",
    "X": "Cryo Regisvine",
    "Y": "Cryo Hypostasis",
    "Z": "Anemo Hypostasis"
}

client = discord.Client()
@client.event
async def on_ready():
    print("Your best campanion {} is here".format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!hello"):
        menu = ""
        for key, value in domains.items():
            menu += "{}: {}\n".format(key, value)
        await message.channel.send("Hi Travalers @everyone! Are you going to join the coop today at 10.30pm?\n" + menu)

    if message.content.startswith("!querystats"):
        cookies = {"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"}
        gClient = genshin.GenshinClient(cookies)

        data = await gClient.get_user(int(message.content[11:]))
        for field in data.explorations:
            reply = ""

            async with aiohttp.ClientSession() as session:
                async with session.get(field.icon) as resp:
                    if resp.status != 200:
                        return await message.channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(file=discord.File(data, 'cool_image.png'))

            reply +=  "{}\n".format(field.name) + "-" * 83 + "\n" \
                    + "{}% explored\n".format(field.percentage)
            if field.type == "Reputation":
                reply += "{} level: {}\n".format(field.type, field.level)
            if len(field.offerings) > 0:
                for o in field.offerings:
                    reply += "{} offering level: {}\n".format(o.name, o.level)
            reply += "=" * 50 + "\n"

            await message.channel.send(reply)

        await gClient.close()
    
    if message.content.startswith("!character"):
        cookies = {"ltuid": 131897908, "ltoken": "PUvLWxC9lWijYCyi8ewhsxj3riKLc763kB85JPuH"}
        gClient = genshin.GenshinClient(cookies)

        data = await gClient.get_partial_user(int(message.content[11:]))

        await message.channel.send(f"User has a total of {len(data.characters)} characters")
        reply = ""
        for char in data.characters:
            reply += f"{char.rarity}* {char.name:20} | lvl {char.level:2} C{char.constellation}" + "\n"
        await message.channel.send(reply)

        await gClient.close()


load_dotenv()
client.run(os.getenv('TOKEN'))