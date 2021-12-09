import discord
from database.domains import domains
from database.coop import Coop


class DomainDropdown(discord.ui.Select):
    def __init__(self, label):
        self.tag = label
        options = []

        for name, material in domains[label].items():
            options.append(discord.SelectOption(label=name, description=material))

        super().__init__(
            placeholder="Choose the domain(s) you want to farm today...",
            min_values=1,
            max_values=len(domains[label]),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            if self.tag == "Ley Line Outcrops":
                Coop.data[interaction.user.id].leyline = []
                data = Coop.data[interaction.user.id].leyline
            elif self.tag == "Weapon Ascension Materials":
                Coop.data[interaction.user.id].weapon = []
                data = Coop.data[interaction.user.id].weapon
            elif self.tag == "Talent Books":
                Coop.data[interaction.user.id].talent = []
                data = Coop.data[interaction.user.id].talent
            elif self.tag == "Artifacts":
                Coop.data[interaction.user.id].artifact = []
                data = Coop.data[interaction.user.id].artifact
            elif self.tag == "Trounce Domains":
                Coop.data[interaction.user.id].trounce = []
                data = Coop.data[interaction.user.id].trounce
            elif self.tag == "World Boss":
                Coop.data[interaction.user.id].world_boss = []
                data = Coop.data[interaction.user.id].world_boss
            ret = ""
            for val in self.values:
                ret += f"You're attending {val}\n"
                data.append(val)
            msg = await interaction.channel.fetch_message(Coop.message_id)
            embed = discord.Embed(title="Coop JSON here", description=f"```{Coop.convert_to_json()}```")
            await msg.edit(embed=embed)
            await interaction.response.send_message(ret, ephemeral=True)
        except:
            await interaction.response.send_message("You're not coming today!", ephemeral=True)


class DomainDropdownView(discord.ui.View):
    def __init__(self, domains):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(DomainDropdown(domains))