import discord
from discord.ext import commands
from discord.ext.commands import BadArgument
from discord.utils import get
import mysql.connector
from settings import host, user, passwd, database, default_color, footer, prefix, modrole, botname, red_color
import json
import asyncio


async def ticket_create(self, bericht, member, db, cursor, guild):
    await self.client.wait_until_ready()

    await asyncio.sleep(0.2)
    db.commit()

    cursor.execute(f"SELECT * FROM tickets WHERE member_id = {member.id}")
    ticket_data = cursor.fetchone()

    if ticket_data is not None:
        await member.send("Je hebt al een ticket open.")
    else:
        with open("data/tickets.json", "r") as read_content:
            data = json.load(read_content)

        ticket_number = data['ticketnummer']
        read_content.close()

        ticket_category = get(bericht.guild.categories, name="▬▬ Tickets ▬▬")
        ticket_channel = await bericht.guild.create_text_channel(f"ticket-{ticket_number:04}", category=ticket_category)

        sql_ids = f"INSERT INTO tickets (channel_id, member_id) VALUES (%s, %s)"
        record = (ticket_channel.id, member.id)
        cursor.execute(sql_ids, record)
        db.commit()

        await ticket_channel.set_permissions(bericht.guild.get_role(bericht.guild.id), send_messages=False, read_messages=False, add_reactions=False, external_emojis=False)
        await ticket_channel.set_permissions(member, send_messages=False, read_messages=True, embed_links=True, attach_files=True, read_message_history=True)

        ticket_embed = discord.Embed(
            description="Bedankt voor het maken van een ticket! Kies eerst je categorie.\n"
                        "Kies de meest gepaste categorie. Je hebt 90 seconden om te kiezen.\n"
                        "Daarna wordt je ticket gesloten en moet je een nieuw ticket aanmaken.\n\n"
                        "1️⃣ **Algemeen Ticket**"
                        "\n2️⃣ **Partnership**"
                        "\n3️⃣ **Staff Sollicitatie**"
                        "\n4️⃣ **Discord Awards**",
            color=default_color
        )
        ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        ticket_embed.set_thumbnail(url=member.avatar_url)
        ticket_embed.set_footer(text=footer)
        ticket_message = await ticket_channel.send(embed=ticket_embed)

        emote_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        doorgaan = False
        reden = "ERROR"

        for emote in emote_list:
            await ticket_message.add_reaction(emote)

        def check(reactie, gebruiker):
            return gebruiker == member and str(reactie.emoji) in emote_list

        while True:
            try:
                reaction, ticketcreator = await self.client.wait_for("reaction_add", timeout=90, check=check)

                if str(reaction.emoji) == emote_list[0]:
                    reden = "Algemeen Ticket"
                    doorgaan = True
                    break
                elif str(reaction.emoji) == emote_list[1]:
                    reden = "Partnership"
                    doorgaan = True
                    break
                elif str(reaction.emoji) == emote_list[2]:
                    reden = "Staff Sollicitatie"
                    doorgaan = True
                    break
                elif str(reaction.emoji) == emote_list[3]:
                    reden = "Discord Awards"
                    doorgaan = True
                    break
            except asyncio.TimeoutError:
                cursor.execute(f"DELETE FROM tickets WHERE member_id = {member.id}")
                db.commit()

                await ticket_channel.delete()

        if doorgaan:
            await ticket_message.clear_reactions()
            await ticket_channel.set_permissions(member, send_messages=True, read_messages=True, embed_links=True, attach_files=True, read_message_history=True)

            with open("data/tickets.json", "r") as read_content:
                data = json.load(read_content)

            data['ticketnummer'] = ticket_number + 1

            with open("data/tickets.json", "w") as outfile:
                json.dump(data, outfile, indent=4)

            read_content.close()

            staff_role = get(guild.roles, name=f"{modrole}")
            await ticket_channel.set_permissions(staff_role, send_messages=True, read_messages=True, embed_links=True, attach_files=True, read_message_history=True)

            ticket_embed = discord.Embed(
                description=f"Bedankt voor het maken van een ticket! We zullen zo snel mogelijk antwoorden.\n"
                            f"Tag ons niet want dat vertraagd het antwoorden alleen maar.\n\n"
                            f"Ticket Eigenaar: {member.mention}\n**Reden:** {reden}",
                color=default_color
            )
            ticket_embed.add_field(name="Ticket Commands", value="!add <naam>\n!remove <naam>\n!close", inline=False)
            ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            ticket_embed.set_thumbnail(url=member.avatar_url)
            ticket_embed.set_footer(text=footer)
            await ticket_message.edit(embed=ticket_embed)

            if str(reaction.emoji) == emote_list[1]:
                await ticket_channel.edit(name=f"partner-{ticket_number:04}", topic=f"{reden}")
                await ticket_channel.send("_ _\nVoltooi deze stappen om een kans te maken op een partnership:"
                                          "\n\n**1.** Meer dan 120 MENSEN in je discord server hebben. (hierop kunnen uitzonderingen worden gemaakt)"
                                          "\n**2.** Stuur een PERMANENTE link van je discord server."
                                          "\n**3.** Vertel waarom je een partnership wilt aangaan.")
            elif str(reaction.emoji) == emote_list[2]:
                await ticket_channel.edit(name=f"sollie-{ticket_number:04}", topic=f"{reden}")
                await ticket_channel.send(f"**Vul het formulier hieronder in om kans te maken om staff te worden bij {botname}.**"
                                          f"\n- __Naam:__"
                                          f"\n- __Leeftijd:__"
                                          f"\n- __Waarom moeten we jou aannemen:__"
                                          f"\n- __Waarom ben jij beter dan iemand anders:__"
                                          f"\n- __Heb je 2FA aanstaan op je discord account:__ Ja/Nee/Ik weet niet wat 2FA is."
                                          f"\n- __Hoelang zit je al in {botname}:__\n*TIP: doe* `{prefix}info` *in* <#793981786560135188>")


class Ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(
            title=f"🎟️ Tickets",
            description=f"Klik op de reactie hieronder om een ticket aan te maken!",
            color=default_color
        )
        em.set_footer(text=footer)
        embed = await ctx.send(embed=em)

        await embed.add_reaction(emoji='🎟️')

        with open("data/tickets.json", "r") as read_content:
            data = json.load(read_content)

        data['ticketchannel'] = embed.channel.id
        data['ticketmessage'] = embed.id

        with open("data/tickets.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

        read_content.close()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        member = payload.user_id
        member = self.client.get_user(member)

        guild = payload.guild_id
        guild = self.client.get_guild(guild)

        with open("data/tickets.json", "r") as read_content:
            data = json.load(read_content)

        setup_channel_id = data['ticketchannel']
        setup_message_id = data['ticketmessage']

        read_content.close()

        if not member.bot and message_id == setup_message_id:
            db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
            cursor = db.cursor()

            cursor.execute(f"SELECT member_id FROM tickets WHERE member_id = {member.id}")
            user_id = cursor.fetchone()

            bericht = await self.client.get_channel(setup_channel_id).fetch_message(setup_message_id)
            await bericht.remove_reaction(emoji=payload.emoji.name, member=member)

            if user_id is not None:
                gebruiker_getinfo = self.client.get_user(member.id)
                await gebruiker_getinfo.send("Je hebt al een ticket open.")
            else:
                await ticket_create(self, bericht, member, db, cursor, guild)
            db.close()

    @commands.command()
    async def close(self, ctx):
        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM tickets WHERE channel_id = {ctx.channel.id}")
        ticket_data = cursor.fetchone()

        staff_role = get(ctx.guild.roles, name=f"{modrole}")
        if ticket_data is not None:
            if staff_role in ctx.author.roles or ctx.author.id == ticket_data[1]:
                await ctx.channel.delete()

                cursor.execute(f"DELETE FROM tickets WHERE channel_id = {ctx.channel.id}")
                db.commit()
        db.close()

    @commands.command()
    async def add(self, ctx, member: discord.Member = None):
        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM tickets WHERE channel_id = {ctx.channel.id}")
        ticket_data = cursor.fetchone()
        db.close()

        staff_role = get(ctx.guild.roles, name=f"{modrole}")
        if ticket_data is not None:
            if staff_role in ctx.author.roles or ctx.author.id == ticket_data[1]:
                if ctx.channel.id == ticket_data[0]:
                    ticket_channel = ctx.message.channel
                    await ticket_channel.set_permissions(member, send_messages=True, read_messages=True,
                                                         add_reactions=True, embed_links=True, attach_files=True,
                                                         read_message_history=True, external_emojis=True)

                    embed = discord.Embed(
                        description=f"{member.mention} is toegevoegd aan dit ticket!",
                        color=default_color
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_footer(text=footer)
                    await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, member: discord.Member = None):
        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM tickets WHERE channel_id = {ctx.channel.id}")
        ticket_data = cursor.fetchone()
        db.close()

        staff_role = get(ctx.guild.roles, name=f"{modrole}")
        if ticket_data is not None:
            if staff_role in ctx.author.roles or ctx.author.id == ticket_data[1]:
                if ctx.channel.id == ticket_data[0]:
                    ticket_channel = ctx.message.channel

                    await ticket_channel.set_permissions(member, send_messages=False, read_messages=False, add_reactions=False,
                                                         embed_links=False, attach_files=False, read_message_history=False, external_emojis=False)

                    ticket_embed = discord.Embed(
                        description=f"{member.mention} is verwijderd van dit ticket!",
                        color=default_color
                    )
                    ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    ticket_embed.set_thumbnail(url=member.avatar_url)
                    ticket_embed.set_footer(text=footer)
                    await ctx.send(embed=ticket_embed)

    @commands.command()
    async def rename(self, ctx, rename_value=None):
        mod_role = get(ctx.guild.roles, name=f"{modrole}")
        if mod_role in ctx.author.roles:
            if rename_value is not None:
                db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
                cursor = db.cursor()

                cursor.execute(f"SELECT * FROM tickets WHERE channel_id = {ctx.channel.id}")
                ticket_data = cursor.fetchone()
                db.close()

                if ticket_data is not None:
                    if ctx.message.channel.id == ticket_data[0]:
                        await ctx.channel.purge(limit=1)
                        rename_channel = ctx.message.channel

                        await rename_channel.edit(name=f"{rename_value.lower()}")

                        ticket_embed = discord.Embed(
                            description=f"Ticket rename naar `{ctx.channel}`",
                            color=default_color
                        )
                        ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        ticket_embed.set_thumbnail(url=ctx.author.avatar_url)
                        ticket_embed.set_footer(text=footer)
                        await ctx.send(embed=ticket_embed)

    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, BadArgument):
            embed = discord.Embed(
                description="**Error!** De opgegeven gebruiker is niet gevonden.",
                color=red_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, BadArgument):
            embed = discord.Embed(
                description="**Error!** De opgegeven gebruiker is niet gevonden.",
                color=red_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Ticket(client))
