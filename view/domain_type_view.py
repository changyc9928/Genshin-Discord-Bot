import discord
from view.dropdown_view import *
from database.domains import domains


class DomainTypeButton(discord.ui.Button["DomainOptionView"]):
    def __init__(self, label: str):
        super().__init__(style=discord.ButtonStyle.blurple, label=label)
        self.label = label

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id in Coop.data:
            await interaction.response.send_message("Please choose the domain(s)/boss(es) you want to farm", view=DomainDropdownView(self.label), ephemeral=True)
        else:
            await interaction.response.send_message("You're not coming today!", ephemeral=True)


class DomainOptionView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DomainTypeButton("Ley Line Outcrops"))   
        self.add_item(DomainTypeButton("Weapon Ascension Materials")) 
        self.add_item(DomainTypeButton("Talent Books"))
        self.add_item(DomainTypeButton("Artifacts"))
        self.add_item(DomainTypeButton("Trounce Domains"))
        self.add_item(DomainTypeButton("World Boss"))