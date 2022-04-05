import discord
from database.domains import Domains
from database.coop import Coop
from utils.embed_formatter import EmbedFormatter


class DomainDropdownEdit(discord.ui.Select):
    def __init__(self, user_id):
        options = []

        # self.weapon = []
        # self.leyline = []
        # self.talent = []
        # self.artifact = []
        # self.world_boss = []
        # self.trounce = []
        for domain in Coop.data[user_id].weapon:
            options.append(discord.SelectOption(
                label=domain, description=Domains.weapon_domains[domain]))
        for domain in Coop.data[user_id].leyline:
            options.append(discord.SelectOption(
                label=domain, description=Domains.leylines[domain]))
        for domain in Coop.data[user_id].talent:
            options.append(discord.SelectOption(
                label=domain, description=Domains.talent_domains[domain]))
        for domain in Coop.data[user_id].artifact:
            options.append(discord.SelectOption(
                label=domain, description=Domains.artifact_domains[domain]))
        for domain in Coop.data[user_id].world_boss:
            options.append(discord.SelectOption(
                label=domain, description=Domains.world_bosses[domain]))
        for domain in Coop.data[user_id].trounce:
            options.append(discord.SelectOption(
                label=domain, description=Domains.trounce_domains[domain]))
        # for name, material in Domains.domains[label].items():
        #     options.append(discord.SelectOption(
        #         label=name, description=material))

        super().__init__(
            placeholder="Choose the booking(s) to cancel...",
            min_values=1,
            max_values=len(options),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            ret = Coop.data[interaction.user.id].remove(self.values)
            if ret == "":
                ret = "Nothing is cancelled"
            msg = await interaction.channel.fetch_message(Coop.message_id)
            embed = discord.Embed(title="Today's Menu")
            embedFormatter = EmbedFormatter(Coop.convert_to_obj(), embed)
            embedFormatter.format_embed()
            await msg.edit(embed=embed)
            await interaction.response.send_message(ret, ephemeral=True)
            # self.__init__(interaction.user.id)
        except Exception as e:
            await interaction.response.send_message("Sorry, Paimon can't cancel your bookings for some reasons T T", ephemeral=True)
            print(e)


class DomainDropdownEditView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(DomainDropdownEdit(user_id))
