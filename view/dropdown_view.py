import discord
from database.domains import Domains
from database.coop import Coop


class DomainDropdown(discord.ui.Select):
    def __init__(self, label):
        self.tag = label
        options = []

        for name, material in Domains.domains[label].items():
            options.append(discord.SelectOption(
                label=name, description=material))

        super().__init__(
            placeholder="Choose the domain(s) you want to farm today...",
            min_values=0,
            max_values=len(Domains.domains[label]),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            ret = Coop.data[interaction.user.id].book(self.tag, self.values)
            msg = await interaction.channel.fetch_message(Coop.message_id)
            embed = discord.Embed(title="Coop JSON here",
                                  description=f"```{Coop.convert_to_json()}```")
            await msg.edit(embed=embed)
            await interaction.response.send_message(ret, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Sorry, Paimon can't record book your domain for some reasons T T", ephemeral=True)
            print(e)


class DomainDropdownView(discord.ui.View):
    def __init__(self, domains):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(DomainDropdown(domains))
