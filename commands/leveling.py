import discord
from discord.ext import commands
from random import randint
from discord.utils import get
import mysql.connector
from settings import host, user, passwd, database, default_color, footer, command_channels
import asyncio


class LevelingSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if not retry_after:
                db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
                cursor = db.cursor()
                random_exp = randint(3, 7)

                cursor.execute(f"SELECT user_id FROM levels WHERE user_id = {message.author.id}")
                user_id = cursor.fetchone()

                if user_id is None:
                    instert_new_user_id = "INSERT INTO levels (user_id, experience, berichten, level) VALUES (%s, %s, %s, %s)"
                    lvl_record = (message.author.id, random_exp, 1, 0)
                    cursor.execute(instert_new_user_id, lvl_record)
                    db.commit()
                    experience = random_exp
                    lvl_start = 0
                else:
                    cursor.execute(f"SELECT * FROM levels WHERE user_id = {message.author.id}")
                    level_data = cursor.fetchone()
                    experience = level_data[1] + random_exp
                    lvl_start = level_data[3]

                    cursor.execute(f"UPDATE levels SET experience = experience + {random_exp}, berichten = berichten + 1 WHERE user_id = {message.author.id}")
                    db.commit()

                level_up_channel = self.client.get_channel(793981786560135188)

                # if experience <= 30:
                #     lvl_end = 0
                # elif 30 < experience <= 70:
                #     lvl_end = 1
                # elif 70 < experience <= 120:
                #     lvl_end = 2
                # elif 120 < experience <= 160:
                #     lvl_end = 3
                # elif 160 < experience <= 220:
                #     lvl_end = 4
                # else:
                lvl_end = int(experience ** (1 / 3.35))

                if lvl_start < lvl_end:
                    if lvl_end >= 5:
                        role = get(message.guild.roles, id=714036438659760159)
                        await message.author.add_roles(role)
                    if lvl_end >= 10:
                        role = get(message.guild.roles, id=714036464404398094)
                        await message.author.add_roles(role)
                    if lvl_end >= 20:
                        role = get(message.guild.roles, id=714036480724566057)
                        await message.author.add_roles(role)
                    if lvl_end >= 25:
                        role = get(message.guild.roles, id=714036496960847902)
                        await message.author.add_roles(role)
                    if lvl_end >= 30:
                        role = get(message.guild.roles, id=773957810135760956)
                        await message.author.add_roles(role)

                    level_embed = discord.Embed(
                        title=f"{message.author.display_name}",
                        description=f"{message.author.mention} is nu level **{lvl_end}**!",
                        color=default_color
                    )
                    level_embed.set_thumbnail(url=message.author.avatar_url)
                    level_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    level_embed.set_footer(text=footer)
                    await level_up_channel.send(embed=level_embed)

                    cursor.execute(f"UPDATE levels SET level = {lvl_end} WHERE user_id = {message.author.id}")
                    db.commit()
                db.close()

    @commands.command(aliases=["level"])
    async def rank(self, ctx, *, member: discord.Member = None):
        if str(ctx.channel) in command_channels:
            if member is None:
                member = ctx.author

            db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM levels WHERE user_id = {member.id}")
            lvl_data = cursor.fetchone()
            level = lvl_data[3]
            berichten = lvl_data[2]
            exp = lvl_data[1]
            db.close()

            accuraat_level = round(exp ** (1 / 3.35), 2)
            voortgang = int((accuraat_level - int(level)) * 100)

            lengte_gekleurdebar = round(voortgang / 5)
            lengte_bar = 20 - lengte_gekleurdebar
            voortgang_bar = "❚" * lengte_gekleurdebar
            rest_bar = "❘" * lengte_bar

            voortgang = f"{voortgang_bar}{rest_bar} ➼ {voortgang}%"

            level_embed = discord.Embed(
                title=f"{member.display_name}",
                description=f"**Voortgang**\n{voortgang}",
                color=default_color
            )
            level_embed.add_field(name="Level", value=f"{level}", inline=True)
            level_embed.add_field(name="Berichten", value=f"{berichten}", inline=True)
            level_embed.set_thumbnail(url=member.avatar_url)
            level_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            level_embed.set_footer(text=footer)
            await ctx.send(embed=level_embed)

    @commands.command()
    async def levels(self, ctx, page=1):
        if str(ctx.channel) in command_channels:
            db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
            cursor = db.cursor()

            offset = (page - 1) * 10
            leaderboard_zin = ""
            volgnummer = offset

            langste_regel = 0

            cursor.execute(f"SELECT * FROM levels ORDER BY berichten DESC LIMIT 10 OFFSET {offset}")
            result = cursor.fetchall()
            for row in result:
                volgnummer = volgnummer + 1
                volgnummer_prefix = f"{volgnummer}."
                lengte_volgnummer_prefix = len(volgnummer_prefix)
                aantal_spaties = 6 - lengte_volgnummer_prefix
                spatie_prefix = " " * aantal_spaties
                volgnummer_prefix = spatie_prefix + volgnummer_prefix

                try:
                    top_names = self.client.get_user(row[0])
                except AttributeError:
                    top_names = "Onbekend#0000"

                aantal_berichten = row[2]
                lengte_aantal_berichten = len(str(aantal_berichten))
                aantal_spaties = 9 - lengte_aantal_berichten
                spatie_prefix = " " * aantal_spaties
                aantal_berichten_prefix = spatie_prefix + str(aantal_berichten)

                nieuwe_zin = f"{volgnummer_prefix} | {aantal_berichten_prefix} | {top_names}\n"
                leaderboard_zin = leaderboard_zin + nieuwe_zin

                if len(nieuwe_zin) > langste_regel:
                    langste_regel = len(nieuwe_zin)

            if leaderboard_zin == "":
                leaderboard_zin = "Geen data gevonden!"

            cursor.execute(f"SELECT berichten FROM levels WHERE berichten != 0")
            max_pages_tuple = cursor.fetchall()
            max_pages = len(max_pages_tuple)

            if max_pages % 10 != 0:
                max_pages = max_pages // 10 + 1
            else:
                max_pages = max_pages // 10

            header = "Plaats | Berichten | Gebruiker"

            if len(header) > langste_regel:
                langste_regel = len(header)

            seperator = "=" * langste_regel

            embed = discord.Embed(
                title=f"Leaderboard Levels",
                description=f"```md\n"
                            f"{header}\n{seperator}\n{leaderboard_zin}"
                            f"\n```",
                color=default_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=f"{footer} | Pagina {page}/{max_pages}")
            leaderboard_message = await ctx.send(embed=embed)

            await leaderboard_message.add_reaction("◀️")
            await leaderboard_message.add_reaction("▶️")

            def check(reactie, gebruiker):
                return gebruiker == ctx.author and str(reactie.emoji) in ["◀️", "▶️"]

            while True:
                try:
                    reaction, member = await self.client.wait_for("reaction_add", timeout=30, check=check)

                    if str(reaction.emoji) == "▶️" and page != max_pages:
                        page += 1
                        await leaderboard_message.remove_reaction(reaction, member)
                        nieuwe_pagina = True
                    elif str(reaction.emoji) == "◀️" and page > 1:
                        page -= 1
                        await leaderboard_message.remove_reaction(reaction, member)
                        nieuwe_pagina = True
                    else:
                        await leaderboard_message.remove_reaction(reaction, member)
                        nieuwe_pagina = False

                    if nieuwe_pagina:
                        offset = (page - 1) * 10
                        leaderboard_zin = ""
                        volgnummer = offset

                        cursor.execute(f"SELECT * FROM maxerg_levels ORDER BY berichten DESC LIMIT 10 OFFSET {offset}")
                        result = cursor.fetchall()
                        for row in result:
                            volgnummer = volgnummer + 1
                            volgnummer_prefix = f"{volgnummer}."
                            lengte_volgnummer_prefix = len(volgnummer_prefix)
                            aantal_spaties = 6 - lengte_volgnummer_prefix
                            spatie_prefix = " " * aantal_spaties
                            volgnummer_prefix = spatie_prefix + volgnummer_prefix

                            try:
                                top_names = self.client.get_user(row[0])
                            except AttributeError:
                                top_names = "Onbekend#0000"

                            aantal_berichten = row[2]
                            lengte_aantal_berichten = len(str(aantal_berichten))
                            aantal_spaties = 9 - lengte_aantal_berichten
                            spatie_prefix = " " * aantal_spaties
                            aantal_berichten_prefix = spatie_prefix + str(aantal_berichten)

                            nieuwe_zin = f"{volgnummer_prefix} | {aantal_berichten_prefix} | {top_names}\n"
                            leaderboard_zin = leaderboard_zin + nieuwe_zin

                            if len(nieuwe_zin) > langste_regel:
                                langste_regel = len(nieuwe_zin)

                        if leaderboard_zin == "":
                            leaderboard_zin = "Geen data gevonden!"

                        if len(header) > langste_regel:
                            langste_regel = len(header)

                        seperator = "=" * langste_regel

                        embed = discord.Embed(
                            title=f"Leaderboard Levels",
                            description=f"```md\n"
                                        f"{header}\n{seperator}\n{leaderboard_zin}"
                                        f"\n```",
                            color=default_color
                        )
                        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        embed.set_footer(text=f"{footer} | Pagina {page}/{max_pages}")
                        await leaderboard_message.edit(embed=embed)
                except asyncio.TimeoutError:
                    await leaderboard_message.clear_reaction("◀️")
                    await leaderboard_message.clear_reaction("▶️")
                    break
            db.close()


def setup(client):
    client.add_cog(LevelingSystem(client))
