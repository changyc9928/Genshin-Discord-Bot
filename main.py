import discord
import genshin
import os

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


bot = PaimonBot()


@bot.command()
async def coop(ctx: commands.Context):
    embed = discord.Embed(title="Coop JSON here", description="```{}```")
    msg = await ctx.send("@everyone Hi Travalers, are you coming today?\n -- Pressing skipping button will clear all your data.\n -- Click on change time button to delay or move forward your online time (default: 10.30 pm).", view=AttendingView(bot), embed=embed)
    Coop.message_id = msg.id


load_dotenv()
bot.run(os.getenv('TOKEN'))