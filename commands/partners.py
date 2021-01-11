import discord
from discord.ext import commands
from settings import default_color, footer


class LevelingSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 86400, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            partner_channels = ['🤝│partners', '👀│zelf-promo']
            if str(message.channel) in partner_channels:
                bucket = self.cd_mapping.get_bucket(message)
                retry_after = bucket.update_rate_limit()
                if retry_after:
                    embed = discord.Embed(
                        color=default_color
                    )
                    embed.add_field(name='Informatie', value='Je mag maar 1x per 24u een bericht sturen.', inline=False)
                    embed.add_field(name='Kopie Bericht', value=f'{message.content}', inline=False)
                    embed.set_author(name=f"{self.client.user.display_name} - Promotie", icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=footer)
                    await message.author.send(embed=embed)
                    await message.delete()


def setup(client):
    client.add_cog(LevelingSystem(client))
