from discord.ext import commands
import discord
from settings import default_color, footer
from datetime import datetime


class OnEvents(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        channel_id = payload.channel_id

        if int(channel_id) != 794334851335061544:
            doorgaan = True
            event_channel = self.client.get_channel(794334851335061544)

            message_id = payload.message_id
            cached_message = payload.cached_message

            channel = self.client.get_channel(channel_id)

            embed = discord.Embed(
                title="Event: Message Delete",
                color=default_color,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Message ID", value=f"{message_id}", inline=True)
            embed.add_field(name="Channel ID", value=f"{channel.mention}", inline=True)

            if cached_message is not None:
                try:
                    member = payload.cached_message.author.id
                    user = self.client.get_user(member)
                    embed.add_field(name="Gebruiker", value=f"{user}", inline=True)

                    if user.bot:
                        doorgaan = False
                except AttributeError:
                    pass

            if doorgaan:
                embed.set_footer(text=footer)
                await event_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        event_channel = self.client.get_channel(794334851335061544)

        embed = discord.Embed(
            title="Event: Member Join",
            color=default_color,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="User", value=f"{member}", inline=True)
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.set_footer(text=footer)
        await event_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        event_channel = self.client.get_channel(794334851335061544)

        embed = discord.Embed(
            title="Event: Member Remove",
            color=default_color,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="User", value=f"{member}", inline=True)
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.set_footer(text=footer)
        await event_channel.send(embed=embed)

    # bugs: User field does @username not @name
    # Docs: https://discordpy.readthedocs.io/en/latest/api.html#discord.on_member_update
    # @commands.Cog.listener()
    # async def on_member_update(self, before, after):
    #     event_channel = self.client.get_channel(794334851335061544)
    #
    #     if before.nick != after.nick:
    #         if after.nick is None:
    #             new_value = before.name
    #         else:
    #             new_value = after.nick
    #
    #         member = before.guild.get_member(before)
    #
    #         embed = discord.Embed(
    #             title="Event: Member Update",
    #             color=default_color,
    #             datetime=datetime.now()
    #         )
    #         embed.add_field(name="User", value=f"{member}", inline=True)
    #         embed.add_field(name="New Username", value=f"{new_value}", inline=True)
    #         embed.set_footer(text=footer)
    #         await event_channel.send(embed=embed)

    # NOT YET STARTED: https://discordpy.readthedocs.io/en/latest/api.html#discord.on_user_update
    # @commands.Cog.listener()
    # async def on_user_update(self, before, after):
    #     event_name = ""
    #     description = ""
    #     await send_embed(self, event_name, description)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        event_channel = self.client.get_channel(794334851335061544)

        embed = discord.Embed(
            title="Event: Invite Created",
            color=default_color,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="User", value=f"{invite.inviter.mention}", inline=True)
        embed.add_field(name="Channel", value=f"{invite.channel.mention}", inline=True)
        embed.add_field(name="Invite Code", value=f"{invite.code}", inline=True)
        embed.set_footer(text=footer)
        await event_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        event_channel = self.client.get_channel(794334851335061544)

        embed = discord.Embed(
            title="Event: Invite Deleted",
            color=default_color,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Invite Code", value=f"{invite.code}", inline=True)
        embed.set_footer(text=footer)
        await event_channel.send(embed=embed)


def setup(client):
    client.add_cog(OnEvents(client))
