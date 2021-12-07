import discord
from view.domain_type_view import DomainOptionView


class AttendingButton(discord.ui.Button["AttendingView"]):
    def __init__(self, label: str, style: discord.ButtonStyle):
        super().__init__(style=style, label=label)
        self.label = label

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if self.label == "Coming":
            await interaction.response.send_message(f"Please indicate what are you farming today from the list below 😃", view=DomainOptionView(), ephemeral=True)
        else:
            await interaction.response.send_message(f"{user} is not coming!")
            # reset his coop data


class AttendingView(discord.ui.View):
    # @discord.ui.button(label="Coming", style=discord.ButtonStyle.success)
    # async def attend(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     user = interaction.user
    #     await interaction.response.send_message(f"{user} is coming!", view=DomainOptionView(), ephemeral=True)

    # @discord.ui.button(label="Skipping", style=discord.ButtonStyle.danger)
    # async def attend(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     user = interaction.user
    #     await interaction.response.send_message(f"{user} is skipping!")
    def __init__(self):
        super().__init__()
        self.add_item(AttendingButton("Coming", discord.ButtonStyle.success))
        self.add_item(AttendingButton("Skipping", discord.ButtonStyle.danger))