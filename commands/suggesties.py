import discord
from discord.ext import commands
from settings import footer, default_color, red_color
import asyncio


class CommandsSuggesties(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def suggestie(self, ctx, *, suggestie=None):
        await ctx.message.delete()

        if suggestie is not None:
            suggestie_channel = self.client.get_channel(793992789724495914)

            embed = discord.Embed(
                title=f"Suggestie van {ctx.author}",
                description=f"{suggestie}",
                color=default_color
            )
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=footer)
            bericht = await suggestie_channel.send(embed=embed)

            emote_list = ['a:duimpje_omhoog:793960986452426772', 'a:duimpje_omlaag:793960986574061618']

            for emote in emote_list:
                await bericht.add_reaction(emoji=emote)
        else:
            error_bericht = await ctx.send("Je moet een geldige suggestie meegeven.")
            await asyncio.sleep(3)
            await error_bericht.delete()

    @suggestie.error
    async def suggestie_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {round(error.retry_after, 2)}s wachten om deze command opnieuw te gebruiken.",
                color=red_color
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(CommandsSuggesties(client))
