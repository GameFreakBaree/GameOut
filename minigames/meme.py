import discord
from discord.ext import commands
import random
from settings import default_color
import praw

reddit = praw.Reddit(
    client_id='zeZ0OueaRlT3Cg',
    client_secret='RRa0GnjxVpqtBgnjvIH26zM4y23-5g',
    username='GameFreakBaree',
    password='gG3pc0BqZW0*5Os4ch%E^eA$^nsjXt',
    user_agent='pythonpraw'
)


class Memes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        minigame_channels = ['🤡│memes', '🔒│bots']
        if str(ctx.channel) in minigame_channels:
            subreddit = reddit.subreddit("memes")
            all_subs = []

            async with ctx.channel.typing():
                top = subreddit.top(limit=50)

                for submission in top:
                    all_subs.append(submission)

                random_sub = random.choice(all_subs)

            embed = discord.Embed(
                color=default_color
            )
            embed.set_image(url=f"{random_sub.url}")
            embed.set_author(name=f"{random_sub.title}", url=f"{random_sub.url}")
            embed.set_footer(text=f"👍 {random_sub.score} | 💬 {random_sub.num_comments}")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Memes(client))
