import discord
import re

from view.domain_type_view import DomainOptionView
from database.coop import Coop
from utils.embed_formatter import EmbedFormatter


class AttendingButton(discord.ui.Button["AttendingView"]):
    def __init__(self, label: str, style: discord.ButtonStyle, bot: discord.ext.commands.bot):
        super().__init__(style=style, label=label)
        self.label = label
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        msg = await interaction.channel.fetch_message(Coop.message_id)
        if self.label == "Coming":
            Coop.add_user(user)
            await interaction.response.send_message(f"Paimon wonder what kind of domains are you farming today from the list below 🤔", view=DomainOptionView(), ephemeral=True)
        elif self.label == "Skipping":
            # reset his coop data
            Coop.deregister_user(user)
            # await interaction.response.send_message(f"{user} is not coming!")
        elif self.label == "Set time":
            if user.id not in Coop.data or Coop.data[user.id].attend == False:
                await interaction.response.send_message(f"Hey {user.name}! You're not coming! Please tell Paimon that you're coming before changing your online time.")
                return

            def check(m):
                return re.match("([0-1][0-9]|2[0-3])[0-5][0-9]", m.content) is not None and m.channel == interaction.channel

            ask = await interaction.response.send_message(f"What time you want to want instead in 24 hour time (HHMM)? {user.mention}")
            response = await self.bot.wait_for("message", check=check)
            Coop.data[user.id].change_time(response.content)
            confirm = await interaction.channel.send(f"@everyone, {response.author.mention} has changed his/her online time to {Coop.data[user.id].time}.")
            await ask.delete_original_message()
            await response.delete()
            # await confirm.delete(delay=2)
        embed = discord.Embed(title="Today's Menu")
        embedFormatter = EmbedFormatter(Coop.convert_to_obj(), embed)
        embedFormatter.format_embed()
        await msg.edit(embed=embed)


class AttendingView(discord.ui.View):
    def __init__(self, bot: discord.ext.commands.bot):
        super().__init__(timeout=None)
        self.add_item(AttendingButton(
            "Coming", discord.ButtonStyle.success, bot))
        self.add_item(AttendingButton(
            "Skipping", discord.ButtonStyle.danger, bot))
        self.add_item(AttendingButton(
            "Set time", discord.ButtonStyle.secondary, bot))
