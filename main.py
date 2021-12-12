import discord
import os
import datetime
import asyncio
import genshin
import csv

from database.coop import Coop
from discord.ext import commands
from dotenv.main import load_dotenv
from view.attending_view import AttendingView


class PaimonBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"))

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        time = datetime.datetime.now(datetime.timezone(datetime.timedelta(
            hours=8))).replace(hour=18, minute=30, second=0, microsecond=0)
        await self.coop(gap=1440, time=time)
        await self.reset_coop(time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
            hours=8))).replace(hour=14, minute=30, second=0, microsecond=0))

    def seconds_until(self, future_exec):
        # given_time = datetime.time(hours, minutes)
        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8)))
        # future_exec = datetime.datetime.combine(now, given_time)
        # if (future_exec - now).seconds < 60:  # If we are past the execution, it will take place tomorrow
        #     future_exec = datetime.datetime.combine(now + datetime.timedelta(minutes=1), given_time) # days always >= 0

        return (future_exec - now).total_seconds()

    async def greet(self):
        channel = self.get_channel(915621292936396821)
        Coop.load_json()
        des = Coop.convert_to_json()
        embed = discord.Embed(title="Coop JSON here",
                              description=f"```{des}```")
        msg = await channel.send("@everyone Hi Travalers, are you coming today?\n -- Pressing skipping button will clear all your data.\n -- Click on change time button to delay or move forward your online time (default: 10.30 pm).", view=AttendingView(bot), embed=embed)
        Coop.message_id = msg.id

    async def coop(self, gap=1, time=datetime.datetime.now() + datetime.timedelta(seconds=5)):
        while True:  # Or change to self.is_running or some variable to control the task
            delta = self.seconds_until(time)
            if delta < 0:
                return
            # Will stay here until your clock says 11:58
            await asyncio.sleep(delta)

            await self.greet()

            # print(f"{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))}")
            time += datetime.timedelta(minutes=gap)

    async def reset_coop(self, gap=1440, time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
            hours=8))).replace(hour=4, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)):
        while True:
            delta = self.seconds_until(time)
            if delta < 0:
                return
            await asyncio.sleep(delta)
            Coop.reset_data()
            time += datetime.timedelta(minutes=gap)
            await self.get_channel(915621292936396821).send("Coop data reset")


bot = PaimonBot()


@bot.command()
async def coop(ctx: commands.Context):
    await bot.greet()


@bot.command()
async def reset(ctx: commands.Context):
    await bot.reset_coop(gap=1, time=datetime.datetime.now(datetime.timezone(datetime.timedelta(
        hours=8))) + datetime.timedelta(seconds=5))


@bot.command()
async def primo(ctx: commands.Context, url: str = None):
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
    cookies = {"ltuid": 131897908,
               "ltoken": "PUvLWxC9lWijYCyi8ewhsxj3riKLc763kB85JPuH"}
    client = genshin.GenshinClient(cookies)
    client.authkey = genshin.extract_authkey(url)
    freq = {}
    # kind='primogem' id=1628258400000123727 uid=828918158 time=datetime.datetime(2021, 8, 6, 22, 3, 6, tzinfo=datetime.timezone.utc) amount=10 reason_id=1049 reason='Achievement reward'
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

load_dotenv()
bot.run(os.getenv('TOKEN'))
