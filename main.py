import discord
import os
import datetime
import asyncio

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
        time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(hour=18, minute=30, second=0, microsecond=0)
        await self.coop(gap=1440, time=time)

    def seconds_until(self, future_exec):
        # given_time = datetime.time(hours, minutes)
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        # future_exec = datetime.datetime.combine(now, given_time)
        # if (future_exec - now).seconds < 60:  # If we are past the execution, it will take place tomorrow
        #     future_exec = datetime.datetime.combine(now + datetime.timedelta(minutes=1), given_time) # days always >= 0

        return (future_exec - now).total_seconds()
        
    async def greet(self):
        channel = self.get_channel(915621292936396821)
        Coop.load_json()
        des = Coop.convert_to_json()
        embed = discord.Embed(title="Coop JSON here", description=f"```{des}```")
        msg = await channel.send("@everyone Hi Travalers, are you coming today?\n -- Pressing skipping button will clear all your data.\n -- Click on change time button to delay or move forward your online time (default: 10.30 pm).", view=AttendingView(bot), embed=embed)
        Coop.message_id = msg.id

    async def coop(self, gap=1, time=datetime.datetime.now()):
        while True:  # Or change to self.is_running or some variable to control the task
            delta = self.seconds_until(time)
            if delta < 0:
                return
            await asyncio.sleep(delta)  # Will stay here until your clock says 11:58

            await self.greet()

            # print(f"{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))}")
            time += datetime.timedelta(minutes=gap)


bot = PaimonBot()


@bot.command()
async def coop(ctx: commands.Context):
    Coop.load_json()
    des = Coop.convert_to_json()
    embed = discord.Embed(title="Coop JSON here", description=f"```{des}```")
    msg = await ctx.send("@everyone Hi Travalers, are you coming today?\n -- Pressing skipping button will clear all your data.\n -- Click on change time button to delay or move forward your online time (default: 10.30 pm).", view=AttendingView(bot), embed=embed)
    Coop.message_id = msg.id


load_dotenv()
bot.run(os.getenv('TOKEN'))