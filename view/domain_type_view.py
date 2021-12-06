import discord
from view.dropdown_view import *


class DomainTypeButton(discord.ui.Button["DomainOptionView"]):
    def __init__(self, label: str):
        super().__init__(style=discord.ButtonStyle.blurple, label=label)
        self.label = label

    async def callback(self, interaction: discord.Interaction):
        if self.label == "Ley Line Outcrops":
            await interaction.response.send_message("Please choose which kind of ley line you want to farm", view=LeyLineDropdownView(), ephemeral=True)
        if self.label == "Weapon Ascension Materials":
            await interaction.response.send_message("Please choose your domain(s) to farm", view=WeaponDropdownView(), ephemeral=True)


class DomainOptionView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DomainTypeButton("Ley Line Outcrops"))   
        self.add_item(DomainTypeButton("Weapon Ascension Materials")) 
        self.add_item(DomainTypeButton("Talent Books"))
        self.add_item(DomainTypeButton("Artifacts"))
        self.add_item(DomainTypeButton("Trounce Domains"))
        self.add_item(DomainTypeButton("World Boss"))