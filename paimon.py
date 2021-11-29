import discord
import genshin
from PIL import Image
import requests
from io import BytesIO


client = discord.Client()
@client.event
async def on_ready():
    print("Your best campanion {} is here".format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!hello"):
        await message.channel.send("Hi Travaler!")

    if message.content.startswith("!querystats"):
        cookies = {"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"}
        gClient = genshin.GenshinClient(cookies)

        data = await gClient.get_user(int(message.content[11:]))
        for field in data.explorations:
            reply = ""
    
            response = requests.get(field.icon)
            img = Image.open(BytesIO(response.content))
            img.save("temp.png")

            with open("temp.png", 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)

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

client.run("OTE0ODE3MjUyMzA0NDk4NzE4.YaSj9Q.hLe4GLhK62LQOvNVdlSGbJQKvpA")