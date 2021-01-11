import discord
from discord.ext import commands
import datetime
from discord.utils import get
import mysql.connector
from settings import host, user, passwd, database, default_color, footer, command_channels


class Informatie(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if str(ctx.channel) in command_channels:
            db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM levels WHERE user_id = {member.id}")
            level_data = cursor.fetchone()

            db.close()

            if level_data is None:
                berichten = (0,)
                level_check = (0,)
            else:
                berichten = level_data[2]
                level_check = level_data[3]

            if member is None:
                member = ctx.author

            joined_correct = member.joined_at.strftime("%d/%m/%Y")

            lvl_role1 = get(member.guild.roles, id=714036438659760159)
            lvl_role2 = get(member.guild.roles, id=714036464404398094)
            lvl_role3 = get(member.guild.roles, id=714036480724566057)
            lvl_role4 = get(member.guild.roles, id=714036496960847902)

            if lvl_role4 in member.roles:
                lvl_role4_emote = "✅"
            else:
                lvl_role4_emote = ":x:"

            if lvl_role3 in member.roles:
                lvl_role3_emote = "✅"
            else:
                lvl_role3_emote = ":x:"

            if lvl_role2 in member.roles:
                lvl_role2_emote = "✅"
            else:
                lvl_role2_emote = ":x:"

            if lvl_role1 in member.roles:
                lvl_role1_emote = "✅"
            else:
                lvl_role1_emote = ":x:"

            info_embed = discord.Embed(
                title=f"{member.display_name}",
                timestamp=datetime.datetime.utcnow(),
                color=default_color
            )
            info_embed.add_field(name="Gebruiker Info",
                                 value=f"ID: {member.id}\n"
                                       f"Gebruikersnaam: {member.display_name}\nTAG: #{member.discriminator}",
                                 inline=False)
            info_embed.add_field(name="Gejoined op", value=joined_correct, inline=True)
            info_embed.add_field(name="Level", value=f"{level_check[0]}", inline=True)
            info_embed.add_field(name="Berichten", value=f"{berichten[0]}", inline=True)
            info_embed.add_field(name="Hoogste Rank", value=member.top_role, inline=True)
            info_embed.add_field(name="Ranks:", value=f"\n{lvl_role4_emote} Level 25+\n{lvl_role3_emote} Level 20+"
                                                      f"\n{lvl_role2_emote} Level 10+\n{lvl_role1_emote} Level 5+\n", inline=True)
            info_embed.set_thumbnail(url=member.avatar_url)
            info_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            info_embed.set_footer(text=footer)
            await ctx.send(embed=info_embed)


def setup(client):
    client.add_cog(Informatie(client))
