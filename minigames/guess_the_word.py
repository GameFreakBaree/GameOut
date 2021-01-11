import discord
from discord.ext import commands
import asyncio
import random
from settings import default_color, footer
import json

t = ["water", "google", "coca-cola", "bloemkool", "limonade",
     "frieten", "python", "apple", "macaroni", "monitor",
     "lasagne", "toetsenbord", "gordijn", "muismat", "skateboard",
     "headset", "rekenmachine", "papier", "discord", "microfoon",
     "developer", "macbook", "roblox", "iphone", "gemeentehuis",
     "slaapzak", "politie", "boekentas", "brandweer", "rugzak",
     "ziekenhuis", "gordijn", "bananen", "airpods", "schoolbanken",
     "limonade", "nintendo", "playstation", "steelseries", "simulator",
     "microsoft", "minecraft", "popmuziek", "minetopia", "verwijderen",
     "nachtkastje", "opslaan", "youtube", "opblazen"]


class GuessTheWord(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            gtw_channel = ["💯│raad-het-woord"]
            if str(message.channel) in gtw_channel:
                with open("data/game_data.json", "r") as read_content:
                    data = json.load(read_content)

                random_word = data['gtw_woord']
                votes = data['votes']
                vote1 = data['vote1']
                vote2 = data['vote2']
                read_content.close()

                vote_list = [vote1, vote2]

                error_emote = "❌"
                check_emote = "✅"

                if message.content.lower() == random_word:
                    await message.add_reaction(emoji=check_emote)

                    embed = discord.Embed(
                        title="Woord Geraden!",
                        description=f"**{message.author.display_name}** heeft het woord geraden!"
                                    f"\n__Woord:__ ` {random_word} `",
                        color=default_color
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=footer)
                    await message.channel.send(embed=embed)

                    random_nieuw_woord = random.choice(t)

                    with open("data/game_data.json", "r") as read_content:
                        data = json.load(read_content)

                    data['gtw_woord'] = str(random_nieuw_woord)
                    data['votes'] = 0
                    data['vote1'] = 0
                    data['vote2'] = 0

                    with open("data/game_data.json", "w") as outfile:
                        json.dump(data, outfile, indent=4)
                    read_content.close()

                    async with message.channel.typing():
                        await asyncio.sleep(3)

                    nieuw_woord_shuffle = list(random_nieuw_woord)
                    random.shuffle(nieuw_woord_shuffle)

                    embed = discord.Embed(
                        title="Raad Het Woord",
                        description=f"Het volgende woord is: ` " + "".join(nieuw_woord_shuffle) + " `",
                        color=default_color
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=f"{footer} | Type '?' om dit woord over te slaan.")
                    await message.channel.send(embed=embed)
                elif message.content.lower() == "?":
                    if votes == 2:
                        if message.author.id not in vote_list:
                            embed = discord.Embed(
                                title="Woord Gereset!",
                                description=f"**Niemand** heeft het woord geraden!"
                                            f"\n__Woord:__ ` {random_word} `",
                                color=default_color
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=f"{footer}")
                            await message.channel.send(embed=embed)

                            random_nieuw_woord = random.choice(t)

                            with open("data/game_data.json", "r") as read_content:
                                data = json.load(read_content)

                            data['gtw_woord'] = str(random_nieuw_woord)
                            data['votes'] = 0
                            data['vote1'] = 0
                            data['vote2'] = 0

                            with open("data/game_data.json", "w") as outfile:
                                json.dump(data, outfile, indent=4)
                            read_content.close()

                            async with message.channel.typing():
                                await asyncio.sleep(3)

                            nieuw_woord_shuffle = list(random_nieuw_woord)
                            random.shuffle(nieuw_woord_shuffle)

                            embed = discord.Embed(
                                title="Raad Het Woord",
                                description=f"Het volgende woord is: ` " + "".join(nieuw_woord_shuffle) + " `",
                                color=default_color
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=f"{footer} | Type '?' om dit woord over te slaan.")
                            await message.channel.send(embed=embed)
                    else:
                        if message.author.id not in vote_list:
                            if 2 - votes == 1:
                                woord = "vote"
                            else:
                                woord = "votes"

                            embed = discord.Embed(
                                title="Raad Het Woord",
                                description=f"Bedankt voor het voten! Nog {2 - votes} {woord} nodig.",
                                color=default_color
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=f"{footer} | Type '?' om dit woord over te slaan.")
                            await message.channel.send(embed=embed)

                            with open("data/game_data.json", "r") as read_content:
                                data = json.load(read_content)

                            data['votes'] += 1
                            if votes + 1 == 1:
                                data['vote1'] = message.author.id
                            elif votes + 1 == 2:
                                data['vote2'] = message.author.id

                            with open("data/game_data.json", "w") as outfile:
                                json.dump(data, outfile, indent=4)
                            read_content.close()
                else:
                    await message.add_reaction(emoji=error_emote)


def setup(client):
    client.add_cog(GuessTheWord(client))
