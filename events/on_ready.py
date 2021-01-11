from discord.ext import commands
import json


class OnReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        bot_naam = self.client.user.display_name
        print(f"[{bot_naam}] De bot is succesvol geladen.")

        stats_channel = self.client.get_channel(793983008641253416)
        guild_ids = stats_channel.guild
        await stats_channel.edit(name=f"✨ Members: {guild_ids.member_count}")

        with open("data/youtube_playlist.json", "r") as read_content:
            data = json.load(read_content)

        data['playlist'] = []

        with open("data/youtube_playlist.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

        read_content.close()


def setup(client):
    client.add_cog(OnReady(client))
