import re
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
from query_graphql import query_image, query_artifact_domains
from database.domains import Domains
from utils.embed_formatter import EmbedFormatter


class PaimonBot(commands.Bot):

    channel = 915621292936396821

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"))

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        ServerData.load_json()
        # print(ServerData.data)

    def seconds_until(self, future_exec):
        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8)))
        return (future_exec - now).total_seconds()

    async def greet(self):
        channel = self.get_channel(PaimonBot.channel)
        with open('images/painmon.gif', 'rb') as f:
            painmonImg = discord.File(f)
            painmonMsg = await channel.send("**Wait while Painmon gets da menu...**", file=painmonImg)
        await Domains.initialize()
        Coop.load_json()
        # des = Coop.convert_to_json()
        embed = discord.Embed(title="Today's Menu")
        coop_json = Coop.convert_to_obj()
        embedFormatter = EmbedFormatter(coop_json, embed)
        embedFormatter.format_embed()
        today_img = discord.File(await query_image(), filename="temp.png")
        await painmonMsg.delete()
        msg = await channel.send("@everyone Minna, are you ikuyo today?\n -- Pressing skipping button will clear all your data.\n -- Click on change time button to delay or move forward your online time (default: 10.30 pm).", view=AttendingView(bot), embed=embed, file=today_img)
        Coop.message_id = msg.id

    async def coop(self, gap=1440, time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
            hours=8))).replace(hour=18, minute=30, second=0, microsecond=0)):
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
            hours=8))).replace(hour=4, minute=0, second=0, microsecond=0)):
        while True:
            delta = self.seconds_until(time)
            if delta < 0:
                time += datetime.timedelta(minutes=gap)
                delta = self.seconds_until(time)
            await asyncio.sleep(delta)
            Coop.reset_data()
            time += datetime.timedelta(minutes=gap)
            await self.get_channel(PaimonBot.channel).send("Coop data reset.")

    async def claim_daily_scheduled(self, gap=1440, time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
            hours=8))).replace(hour=0, minute=30, second=0, microsecond=0)):
        while True:
            delta = self.seconds_until(time)
            if delta < 0:
                time += datetime.timedelta(minutes=gap)
                delta = self.seconds_until(time)
            await asyncio.sleep(delta)
            self.claim_daily()
            time += datetime.timedelta(minutes=gap)

    async def claim_daily(self):
        for uid, _ in ServerData.data.items():
            try:
                client = ServerData.get_client(uid)
            except Exception as err:
                await self.get_channel(PaimonBot.channel).send(f"Painmon couldn't get your connect to {uid}'s client API T_T\n{err}")
                return
            try:
                reward = await client.claim_daily_reward()
            except Exception as err:
                await self.get_channel(PaimonBot.channel).send(f"Painmon couldn't claim {uid}'s daily rewards T_T\n{err}")
            else:
                await self.get_channel(PaimonBot.channel).send(f"Painmon has claimed {reward.amount}x {reward.name} for {uid}")
            await client.close()


bot = PaimonBot()
bot.loop.create_task(bot.coop())
bot.loop.create_task(bot.reset_coop())
bot.loop.create_task(bot.claim_daily())


@bot.command()
async def coop_test(ctx: commands.Context):
    await bot.greet()


@bot.command()
async def reset_test(ctx: commands.Context):
    Coop.reset_data()
    await ctx.send("Manually reset coop data.")


@bot.command()
async def register_test(ctx: commands.Context):
    await ctx.send(f"{ctx.author.mention}, what's your uid?")

    def check_uid(m):
        return re.match("[012568][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", m.content) is not None and m.channel == ctx.channel and m.author == ctx.author

    uid = await bot.wait_for("message", check=check_uid)
    ret = ServerData.register(uid.content)
    if not ret:
        await ctx.send("Your account has already registered...")
        return

    await setAuthkey_test(ctx, uid)

    await setCookies_test(ctx, uid)

    await ctx.send(f"{ctx.author.mention}, Painmon has successfully registered your Genshin account.")


@bot.command()
async def deleteAcc_test(ctx: commands.Context):
    await ctx.send(f"{ctx.author.mention}, what's your uid?")

    def check_uid(m):
        return re.match("[012568][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", m.content) is not None and m.channel == ctx.channel and m.author == ctx.author

    uid = await bot.wait_for("message", check=check_uid)
    ret = ServerData.delete(uid.content)
    if not ret:
        await ctx.send("Painmon can't delete your account for some reasons...")
        return

    await ctx.send(f"{ctx.author.mention}, Painmon has successfully deleted your Genshin account.")


@bot.command()
async def setCookies_test(ctx: commands.Context, uid=None):
    if uid is None:
        await ctx.send(f"{ctx.author.mention}, what's your uid?")

        def check_uid(m):
            return re.match("[012568][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", m.content) is not None and m.channel == ctx.channel and m.author == ctx.author

        uid = await bot.wait_for("message", check=check_uid)

    await ctx.send(f"{ctx.author.mention}, please enter your ltuid, it will be expired in 24 hours. Follow the steps below:")
    await ctx.send(f"go to hoyolab.com\n"
                   "login to your account\n"
                   "press F12 to open inspect mode (aka Developer Tools)\n"
                   "go to Application, Cookies, https://www.hoyolab.com.\n"
                   "copy ltuid and ltoken")

    def check_ltuid(m):
        return re.match("[0-9]*", m.content) is not None and m.channel == ctx.channel and m.author == ctx.author

    ltuid = await bot.wait_for("message", check=check_ltuid)

    await ctx.send(f"{ctx.author.mention}, please enter your ltoken, follow the above steps.")

    def check_ltoken(m):
        return re.match(".*", m.content) is not None and m.channel == ctx.channel and m.author == ctx.author

    ltoken = await bot.wait_for("message", check=check_ltoken)

    ret = ServerData.set_cookies(uid.content, ltoken.content, ltuid.content)
    if not ret:
        await ctx.send("Can't save your cookies for some reasons...")

    await ctx.send(f"{ctx.author.mention}, Painmon has successfully set your cookies.")


@bot.command()
async def setAuthkey_test(ctx: commands.Context, uid=None):
    if uid is None:
        await ctx.send(f"{ctx.author.mention}, what's your uid?")

        def check_uid(m):
            return re.match("[012568][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", m.content) is not None and m.channel == ctx.channel and m.author == ctx.author

        uid = await bot.wait_for("message", check=check_uid)
    await ctx.send(f"{ctx.author.mention}, please enter your authkey, it will be expired in 24 hours. Follow the steps below:")
    await ctx.send(f"Open Genshin Impact in this PC (If you use multiple accounts, please restart the game)\n"
                   "Then open the wish history in the game and wait it to load\n"
                   "Press START on your keyboard, then search for Powershell\n"
                   "Click Windows Powershell, then copy & paste the script below to the Powershell\n"
                   "```iex ((New-Object System.Net.WebClient).DownloadString('https://gist.githubusercontent.com/MadeBaruna/1d75c1d37d19eca71591ec8a31178235/raw/41853f2b76dcb845cf8cb0c44174fb63459920f4/getlink_global.ps1'))```\n"
                   "You can review the script here: https://gist.github.com/MadeBaruna/1d75c1d37d19eca71591ec8a31178235\n"
                   "Press ENTER, and a link will copied to your clipboard\n"
                   "Paste the text here")

    def check_authkey(m):
        return re.match("https://webstatic.*", m.content) is not None and m.channel == ctx.channel and m.author == ctx.author

    authkey = await bot.wait_for("message", check=check_authkey)
    ret = ServerData.set_authkey(uid.content, authkey.content)

    if not ret:
        await ctx.send("Can't save your authkey for some reasons...")
        return

    await ctx.send(f"{ctx.author.mention}, Painmon has successfully set your authkey.")

# @bot.command()
# async def registerAccount(ctx: commands.Context, uid: int):
#     ret = ServerData.register_account(ctx.author.id, uid)
#     if not ret:
#         await ctx.send("Painmon can't register your Genshin account for some reasons...")
#     else:
#         await ctx.send("Painmon has successfully registered your Genshin account!")


@bot.command()
async def primo_test(ctx: commands.Context, uid: str):
    patch_released_date = [
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
        datetime.datetime(2022, 2, 16, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2022, 3, 30, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
        datetime.datetime(2022, 5, 11, tzinfo=datetime.timezone(
            datetime.timedelta(hours=8))),
    ]
    patch_ver = [
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
        "2.4",
        "2.5",
        "2.6",
        "2.7"
    ]
    # cookies = {"ltuid": 131897908,
    #            "ltoken": "PUvLWxC9lWijYCyi8ewhsxj3riKLc763kB85JPuH"}
    try:
        client = ServerData.get_client(uid)
    except Exception as err:
        await ctx.send(f"Painmon couldn't get your connect to your account client API T_T\n{err}")
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
                for i in range(1, len(patch_released_date)):
                    if patch_released_date[i-1] <= trans.time < patch_released_date[i]:
                        key = patch_ver[i-1]
                if key not in freq:
                    freq[key] = {}
                if trans.reason not in freq[key]:
                    freq[key][trans.reason] = 0
                freq[key][trans.reason] += trans.amount
    except Exception as err:
        await ctx.send(f"Painmon can't get your primogem transactions for some reasons...\n{err}")

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
async def wishHistory_test(ctx: commands.Context, uid: str):
    await ctx.send("Key in the banner id(s) you want to query:\nNovice Wishes: 100\nPermanent Wish: 200\nCharacter Event Wish: 301\nWeapon Event Wish: 302")
    banner = set()

    def check(m):
        return m.content in ["100", "200", "301", "302", "end"] and m.channel == ctx.channel and m.author == ctx.author
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

    try:
        client = ServerData.get_client(uid)
    except Exception as err:
        await ctx.send(f"Painmon couldn't get your connect to your account client API T_T\n{err}")
        return
    await ctx.send("Give Painmon a sec plz...")
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


@bot.command()
async def claimDaily_test(ctx: commands.Context):
    await bot.claim_daily()

load_dotenv()
bot.run(os.getenv('TOKEN'))
