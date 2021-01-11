import discord
from discord.ext import commands
from random import randint
from settings import default_color, footer
import json

min_nummer = 1
max_nummer = 1000
vorige_id = 0


class HigherLower(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            hl_channel = ["🏆│hoger-lager"]
            if str(message.channel) in hl_channel:
                global vorige_id
                with open("data/game_data.json", "r") as read_content:
                    data = json.load(read_content)

                luckynumber = data['hl_nummer']
                read_content.close()

                if message.author.id == vorige_id:
                    await message.channel.purge(limit=1)
                else:
                    try:
                        message_inhoud = int(message.content)

                        if message_inhoud > min_nummer:
                            await message.channel.purge(limit=1)
                        elif message_inhoud < max_nummer:
                            await message.channel.purge(limit=1)
                        else:
                            vorige_id = message.author.id

                            higher_emote = "🔼"
                            lower_emote = "🔽"
                            check_emote = "✅"

                            if message_inhoud > luckynumber:
                                await message.add_reaction(emoji=lower_emote)
                            elif message_inhoud < luckynumber:
                                await message.add_reaction(emoji=higher_emote)
                            elif message_inhoud == luckynumber:
                                await message.add_reaction(emoji=check_emote)

                                embed = discord.Embed(
                                    title="Nummer Geraden!",
                                    description=f"**{message.author.display_name}** heeft het nummer geraden!",
                                    color=default_color
                                )
                                embed.set_footer(text=footer)
                                await message.channel.send(embed=embed)

                                random_number = randint(min_nummer, max_nummer)

                                with open("data/game_data.json", "r") as read_content:
                                    data = json.load(read_content)

                                data['hl_nummer'] = random_number

                                with open("data/game_data.json", "w") as outfile:
                                    json.dump(data, outfile, indent=4)

                                read_content.close()
                    except ValueError:
                        await message.channel.purge(limit=1)


def setup(client):
    client.add_cog(HigherLower(client))
