import os

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
    await ctx.send("@everyone Hi Travalers, are you coming today?", view=AttendingView())


load_dotenv()
bot.run(os.getenv('TOKEN'))