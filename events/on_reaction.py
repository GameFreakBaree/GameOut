from discord.ext import commands
from discord.utils import get, find
import discord
from settings import footer, default_color


def role_check(payload, guild):
    role = None

    if payload.emoji.name == "1️⃣":
        role = get(guild.roles, id=793963826340036648)
    elif payload.emoji.name == "2️⃣":
        role = get(guild.roles, id=793963871802097736)
    elif payload.emoji.name == "3️⃣":
        role = get(guild.roles, id=793963885928906803)
    elif payload.emoji.name == "4️⃣":
        role = get(guild.roles, id=793963897002000424)
    elif payload.emoji.name == "5️⃣":
        role = get(guild.roles, id=793963906879586366)

    return role


class OnReaction(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 786981222739214367:
            guild_id = payload.guild_id
            guild = find(lambda g: g.id == guild_id, self.client.guilds)
            member = find(lambda m: m.id == payload.user_id, guild.members)

            role = role_check(payload, guild)

            if role is not None and member is not None:
                if not member.bot:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 786981222739214367:
            guild_id = payload.guild_id
            guild = find(lambda g: g.id == guild_id, self.client.guilds)
            member = find(lambda m: m.id == payload.user_id, guild.members)

            role = role_check(payload, guild)

            if role is not None and member is not None:
                if not member.bot:
                    await member.remove_roles(role)

    @commands.command()
    @commands.is_owner()
    async def roles(self, ctx, *, channel: discord.TextChannel):
        embed = discord.Embed(
            title="Geef jezelf rollen.",
            description=f"<@&793963826340036648>: 1️⃣"
                        f"\n<@&793963871802097736>: 2️⃣"
                        f"\n<@&793963885928906803>: 3️⃣"
                        f"\n<@&793963897002000424>: 4️⃣"
                        f"\n<@&793963906879586366>: 5️⃣",
            color=default_color
        )
        embed.set_footer(text=footer)
        message = await channel.send(embed=embed)

        emote_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

        for emote in emote_list:
            await message.add_reaction(emoji=emote)


def setup(client):
    client.add_cog(OnReaction(client))
