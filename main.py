import discord
import os
import datetime
import asyncio
import csv

from database.members import ServerData
from database.coop import Coop
from discord.ext import commands
from dotenv.main import load_dotenv
from view.attending_view import AttendingView
from query_graphql import query_image


class PaimonBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"))

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        ServerData.load_json()

    def seconds_until(self, future_exec):
        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8)))
        return (future_exec - now).total_seconds()

    async def greet(self):
        channel = self.get_channel(915621292936396821)
        Coop.load_json()
        des = Coop.convert_to_json()
        embed = discord.Embed(title="Coop JSON here",
                              description=f"```{des}```")
        today_img = discord.File(await query_image(), filename="temp.png")
        msg = await channel.send("@everyone Hi Travalers, are you coming today?\n -- Pressing skipping button will clear all your data.\n -- Click on change time button to delay or move forward your online time (default: 10.30 pm).", view=AttendingView(bot), embed=embed, file=today_img)
        Coop.message_id = msg.id

    async def coop(self, gap=2, time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
            hours=8))).replace(hour=20, minute=10, second=0, microsecond=0)):
        while True:  # Or change to self.is_running or some variable to control the task
            delta = self.seconds_until(time)
            while delta < 0:
                time += datetime.timedelta(minutes=gap)
                delta = self.seconds_until(time)
            # Will stay here until your clock says 18:30
            await asyncio.sleep(delta)

            await self.greet()

            # print(f"{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))}")
            time += datetime.timedelta(minutes=gap)

    async def reset_coop(self, gap=1440, time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
            hours=8))).replace(hour=4, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)):
        while True:
            delta = self.seconds_until(time)
            if delta < 0:
                time += datetime.timedelta(minutes=gap)
                delta = self.seconds_until(time)
            await asyncio.sleep(delta)
            Coop.reset_data()
            time += datetime.timedelta(minutes=gap)
            await self.get_channel(915621292936396821).send("Coop data reset")


bot = PaimonBot()
bot.loop.create_task(bot.coop())
bot.loop.create_task(bot.reset_coop())


@bot.command()
async def coop(ctx: commands.Context):
    await bot.greet()


@bot.command()
async def reset(ctx: commands.Context):
    await bot.reset_coop(gap=1, time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
        hours=8))) + datetime.timedelta(seconds=5))


@bot.command()
async def register(ctx: commands.Context):
    ret = ServerData.register(ctx.author.id, ctx.author.name)
    if ret:
        await ctx.send("Paimon has successfully registered you to the server database!")
    else:
        await ctx.send("Paimon can't register you for some reasons...")


@bot.command()
async def setCookies(ctx: commands.Context, ltoken: str, ltuid: int):
    ret = ServerData.set_cookies(ctx.author.id, ltoken, ltuid)
    if not ret:
        await ctx.send("Paimon can't register your cookies for some reasons...")
    else:
        await ctx.send("Paimon has successfully registered your cookies!")


@bot.command()
async def setAuthkey(ctx: commands.Context, uid: int, url: str):
    ret = ServerData.set_authkey(ctx.author.id, uid, url)
    if not ret:
        await ctx.send("Paimon can't register your authkey for some reasons...")
    else:
        await ctx.send("Paimon has successfully registered your authkey!")


@bot.command()
async def registerAccount(ctx: commands.Context, uid: int):
    ret = ServerData.register_account(ctx.author.id, uid)
    if not ret:
        await ctx.send("Paimon can't register your Genshin account for some reasons...")
    else:
        await ctx.send("Paimon has successfully registered your Genshin account!")


@bot.command()
async def primo(ctx: commands.Context, uid: int):
    patch = [
        datetime.datetime(2020, 9, 28, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2020, 11, 11, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2020, 12, 23, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 2, 3, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 3, 17, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 4, 28, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 6, 9, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 7, 21, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 9, 1, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 10, 13, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2021, 11, 24, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2022, 1, 5, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
    ]
    patch_no = [
        "1.0",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.5",
        "1.6",
        "2.0",
        "2.1",
        "2.2",
        "2.3",
        "2.4"
    ]
    # cookies = {"ltuid": 131897908,
    #            "ltoken": "PUvLWxC9lWijYCyi8ewhsxj3riKLc763kB85JPuH"}
    client = ServerData.get_client(ctx.author.id)
    if client is None:
        await ctx.send("Paimon couldn't get your authkey T T")
        return
    client.authkey = ServerData.get_authkey(ctx.author.id, uid)
    if client.authkey is None:
        await ctx.send("Paimon couldn't get your authkey T T")
        await client.close()
        return
    freq = {}
    # kind='primogem' id=1628258400000123727 uid=828918158 time=datetime.datetime(2021, 8, 6, 22, 3, 6, tzinfo=datetime.timezone.utc) amount=10 reason_id=1049 reason='Achievement reward'
    try:
        with open(f'{ctx.author.name}\'s primogems transaction.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "Reason", "Amount"])
            async for trans in client.transaction_log("primogem"):
                writer.writerow([trans.time.strftime(
                    '%Y-%m-%d %H:%M %Z'), trans.reason, trans.amount])
                key = ""
                for i in range(1, len(patch)):
                    if patch[i-1] <= trans.time < patch[i]:
                        key = patch_no[i-1]
                if key not in freq:
                    freq[key] = {}
                if trans.reason not in freq[key]:
                    freq[key][trans.reason] = 0
                freq[key][trans.reason] += trans.amount
    except:
        await ctx.send("Paimon can't get your primogem transactions for some reasons...")

    for key, value in freq.items():
        ret = ""
        total = 0
        ret += f"{key}: \n"
        for reason, amount in value.items():
            ret += f"{reason}: {amount}\n"
            total += amount if amount > 0 else 0
        ret += f"**Total: {total}**\n"
        ret += "\n\n"
        await ctx.send(ret)
    await ctx.send(file=discord.File(f'{ctx.author.name}\'s primogems transaction.csv'))
    os.remove(f'{ctx.author.name}\'s primogems transaction.csv')
    await client.close()


@bot.command()
async def wishHistory(ctx: commands.Context, uid: int):
    await ctx.send("Key in the banner id(s) you want to query:\nNovice Wishes: 100\nPermanent Wish: 200\nCharacter Event Wish: 301\nWeapon Event Wish: 302")
    banner = set()

    def check(m):
        return m.content in ["100", "200", "301", "302", "end"] and m.channel == ctx.channel
    response = await bot.wait_for("message", check=check)
    while response.content.lower() != "end":
        banner.add(int(response.content))
        response = await bot.wait_for("message", check=check)
    banner = list(banner)

    def check_limit(m):
        try:
            return int(m.content) > 1 or int(m.content) == -1
        except:
            return False
    await ctx.send("Any limit to recent n wishes? Type -1 if no otherwise please provide a number (at least 1)")
    response = await bot.wait_for("message", check=check_limit)
    limit = int(response.content)
    if limit == -1:
        limit = None

    client = ServerData.get_client(ctx.author.id)
    if client is None:
        await ctx.send("Paimon couldn't get your authkey T T")
        return
    client.authkey = ServerData.get_authkey(ctx.author.id, uid)
    await ctx.send("OK, please give me a moment...")
    ret = []
    async for wish in client.wish_history(banner, limit=limit):
        if wish.rarity == 5:
            ret.append(
                f"{wish.time} - ***{wish.name} ({wish.rarity}* {wish.type})***\n")
        elif wish.rarity == 4:
            ret.append(
                f"{wish.time} - **{wish.name} ({wish.rarity}* {wish.type})**\n")
        else:
            ret.append(
                f"{wish.time} - {wish.name} ({wish.rarity}* {wish.type})\n")
        await asyncio.sleep(0.5)
    offset = 0
    while offset < len(ret):
        await ctx.send("".join(ret[offset:min(offset+30, len(ret))]))
        offset += 30
    await client.close()

load_dotenv()
bot.run(os.getenv('TOKEN'))
