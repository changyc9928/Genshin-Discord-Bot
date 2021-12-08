import datetime
import discord
import re

from view.domain_type_view import DomainOptionView
from database.coop import Coop, UserData


class AttendingButton(discord.ui.Button["AttendingView"]):
    def __init__(self, label: str, style: discord.ButtonStyle, bot: discord.ext.commands.bot):
        super().__init__(style=style, label=label)
        self.label = label
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        msg = await interaction.channel.fetch_message(Coop.message_id)
        if self.label == "Coming":
            if user.id not in Coop.data:
                Coop.data[user.id] = UserData(user.name)
            await interaction.response.send_message(f"Paimon wonder what kind of domains are you farming today from the list below 🤔", view=DomainOptionView(), ephemeral=True)
        elif self.label == "Skipping":
            # reset his coop data
            if user.id in Coop.data:
                del Coop.data[user.id]
            # await interaction.response.send_message(f"{user} is not coming!")
        elif self.label == "Change time":
            if user.id not in Coop.data:
                await interaction.response.send_message(f"Hey {user.name}! You're not coming! Please tell Paimon that you're coming before changing your online time.")
                return

            def check(m):
                return re.match("([0-1][0-9])|2[0-3][0-5][0-9]", m.content) and m.channel == interaction.channel

            await interaction.response.send_message(f"What time you want to want instead in 24 hour time (HHMM)? {user.name}")
            response = await self.bot.wait_for("message", check=check)
            Coop.data[user.id].time = datetime.datetime.today().replace(hour=int(response.content[:2]), minute=int(response.content[2:]), second=0, microsecond=0).astimezone().strftime('%Y-%m-%d %H:%M %Z')
            await interaction.channel.send(f"{response.author.name}, Paimon has changed your online time to {Coop.data[user.id].time}.")
        embed = discord.Embed(title="Coop JSON here", description=f"```{Coop.convert_to_json()}```")
        await msg.edit(embed=embed)


class AttendingView(discord.ui.View):
    def __init__(self, bot: discord.ext.commands.bot):
        super().__init__()
        self.add_item(AttendingButton("Coming", discord.ButtonStyle.success, bot))
        self.add_item(AttendingButton("Skipping", discord.ButtonStyle.danger, bot))
        self.add_item(AttendingButton("Change time", discord.ButtonStyle.secondary, bot))