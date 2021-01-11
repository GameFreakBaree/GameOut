from discord.ext import commands
import json


class Counting(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            counting_channels = ["➕│tellen"]
            if str(message.channel) in counting_channels:
                with open("data/game_data.json", "r") as read_content:
                    data = json.load(read_content)

                vorige_id = data['last_user']
                number = data['count']
                read_content.close()

                if message.author.id == vorige_id:
                    await message.channel.purge(limit=1)
                else:
                    try:
                        message_inhoud = int(message.content)
                        if message_inhoud == number + 1:
                            await message.add_reaction(emoji='✅')

                            with open("data/game_data.json", "r") as read_content:
                                data = json.load(read_content)

                            data['last_user'] = message.author.id
                            data['count'] += 1

                            with open("data/game_data.json", "w") as outfile:
                                json.dump(data, outfile, indent=4)
                            read_content.close()
                        else:
                            await message.delete()
                    except ValueError:
                        await message.delete()


def setup(client):
    client.add_cog(Counting(client))
