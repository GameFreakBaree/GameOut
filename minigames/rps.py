import datetime
import random
import discord
from discord.ext import commands
from settings import default_color, footer, minigame_channels


def verstuur_rpsembed(self, item_speler, item_bot, uitkomst):
    if uitkomst == "win":
        title = "Je hebt gewonnen!"
        desc = f"Je koos: **{item_speler}**\nDe bot koos: **{item_bot}**\n\nUitkomst: **Je Wint!**"
    elif uitkomst == "lose":
        title = "Je hebt verloren!"
        desc = f"Je koos: **{item_speler}**\nDe bot koos: **{item_bot}**\n\nUitkomst: **Je Verliest!**"
    elif uitkomst == "tie":
        title = "Je hebt gelijkgespeeld!"
        desc = f"Je koos: **{item_speler}**\nDe bot koos: **{item_bot}**\n\nUitkomst: **Gelijkspel!**"
    else:
        title = "ERROR"
        desc = "Er is een fout gebeurt, probeer het opnieuw."

    embed = discord.Embed(
        title=title,
        description=desc,
        color=default_color,
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
    embed.set_footer(text=footer)
    return embed


class RockPaperScissors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sps", "steen-papier-schaar", "rock-paper-scissors"])
    async def rps(self, ctx, *, argument=None):
        if str(ctx.channel) in minigame_channels:
            if argument is None:
                await ctx.send("Dit is geen geldig argument. Probeer opnieuw. (Je kan kiezen uit: steen, papier, schaar) [`!rps schaar`]")
            else:
                t = ["papier", "steen", "schaar"]
                responses = random.choice(t)

                argument = argument.lower()
                if argument == responses:
                    await ctx.send(embed=verstuur_rpsembed(self, argument, responses, "tie"))
                elif argument == "steen":
                    if responses == "papier":
                        await ctx.send(embed=verstuur_rpsembed(self, argument, responses, "lose"))
                    else:
                        await ctx.send(embed=verstuur_rpsembed(self, argument, responses, "win"))
                elif argument == "papier":
                    if responses == "schaar":
                        await ctx.send(embed=verstuur_rpsembed(self, argument, responses, "lose"))
                    else:
                        await ctx.send(embed=verstuur_rpsembed(self, argument, responses, "win"))
                elif argument == "schaar":
                    if responses == "steen":
                        await ctx.send(embed=verstuur_rpsembed(self, argument, responses, "lose"))
                    else:
                        await ctx.send(embed=verstuur_rpsembed(self, argument, responses, "win"))
                else:
                    await ctx.send("Dit is geen geldig argument. Probeer opnieuw. (Je kan kiezen uit: steen, papier, schaar)")


def setup(client):
    client.add_cog(RockPaperScissors(client))
