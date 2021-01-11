from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database


class OnLeave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        stats_channel = self.client.get_channel(793983008641253416)
        guild_ids = stats_channel.guild

        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"DELETE FROM levels WHERE user_id = {member.id}")
        db.commit()
        db.close()

        await stats_channel.edit(name=f"✨ Members: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnLeave(client))
