import discord
import genshin
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
import io
import aiohttp


weapon_domains = {
    ":one:": "Mondsdalt Weapon",
    ":two:": "Liyue Weapon",
    ":three:": "Inazuma Weapon",
}
talent_domains = {
    ":one:": "Mondsdalt Talent",
    ":two:": "Liyue Talent",
    ":three:": "Inazuma Talent"
}
trounce_domains = {
    ":one:": "Wolf",
    ":two:": "Azhdaha",
    ":three:": "Childe",
    ":four:": "La Signora"
}
artifact_domains = {
    ":one:": "Archaic Petra/Retracing Bolide",
    ":two:": "Thundering Fury/Thundersoother",
    ":three:": "Viridescent Venerer/Maiden Beloved",
    ":four:": "Crimson Witch of Flames/Lavawalker",
    ":five:": "Blizzard Strayer/Heart of Depth",
    ":six:": "Tenacity of the Millelith/Pale Flame",
    ":seven:": "Shimenawa's Reminiscence/Emblem of Severed Fate",
    ":eight:": "Husk of Opulent Dreams/Ocean-Hued Clam",
    ":nine:": "Bloodstained Chivalry/Noblesse Oblige"
}
world_bosses = {
    ":one:": "Thunder Manifestation",
    ":two:": "Rhodeia of Loch",
    ":three:": "Pyro Regisvine",
    ":four:": "Pyro Hypostasis",
    ":five:": "Primo Geovishap",
    ":six:": "Perpetual Mechanical Array",
    ":seven:": "Maguu Kenki",
    ":eight:": "Hydro Hypostasis",
    ":nine:": "Golden Wolflord",
    ":zero:": "Geo Hypostasis",
    ":regional_indicator_a:": "Electro Hypostasis",
    ":regional_indicator_b:": "Cryo Regisvine",
    ":regional_indicator_c:": "Cryo Hypostasis",
    ":regional_indicator_d:": "Anemo Hypostasis"
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
        greetings = await message.channel.send("Hi Travalers @everyone! Are you going to join the coop today at 10.30pm?")
        await greetings.add_reaction(u"\u2611")
        await greetings.add_reaction("❌")
        menu = "**Weapon Domains**\n"
        for key, value in weapon_domains.items():
            menu += "{}: {}\n".format(key, value)
        await message.channel.send(menu)
        menu = "**Talent Books Domains**\n"
        for key, value in talent_domains.items():
            menu += "{}: {}\n".format(key, value)
        await message.channel.send(menu)
        menu = "**Artifacts Domains**\n"
        for key, value in artifact_domains.items():
            menu += "{}: {}\n".format(key, value)
        await message.channel.send(menu)
        menu = "**Weekly Bosses**\n"
        for key, value in trounce_domains.items():
            menu += "{}: {}\n".format(key, value)
        await message.channel.send(menu)
        menu = "**World Bosses**\n"
        for key, value in world_bosses.items():
            menu += "{}: {}\n".format(key, value)
        await message.channel.send(menu)

    if message.content.startswith("!querystats"):
        cookies = {"ltuid": 119480035,
                   "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"}
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

            reply += "{}\n".format(field.name) + "-" * 83 + "\n" \
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
        cookies = {"ltuid": 131897908,
                   "ltoken": "PUvLWxC9lWijYCyi8ewhsxj3riKLc763kB85JPuH"}
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
