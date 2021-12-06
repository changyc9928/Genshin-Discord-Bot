import discord
from database.domains import *


class LeyLineDropdown(discord.ui.Select):
    def __init__(self):
        options = []

        for name, material in leylines.items():
            options.append(discord.SelectOption(label=name, description=material))

        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=len(leylines),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        ret = ""
        for val in self.values:
            ret += f"You're attending {val}\n"
        await interaction.response.send_message(ret, ephemeral=True)


class LeyLineDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(LeyLineDropdown())


class WeaponDropdown(discord.ui.Select):
    def __init__(self):
    
        # Set the options that will be presented inside the dropdown
        options = []

        for location, material in weapon_domains.items():
            options.append(discord.SelectOption(label=location, description=material))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=len(weapon_domains),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options.
        ret = ""
        for val in self.values:
            ret += f"You're attending {val}\n"
        await interaction.response.send_message(ret, ephemeral=True)


class WeaponDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(WeaponDropdown())