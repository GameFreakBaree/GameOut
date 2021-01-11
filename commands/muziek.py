import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
from settings import prefix


class Muziek(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @commands.command()
    # async def play(self, ctx, url='https://www.youtube.com/watch?v=pVLmZMjxfjw'):
    #     if ctx.author.voice is None:
    #         await ctx.send("Je moet in een spraak kanaal zitten om de muziek commands te kunnen gebruiken.")
    #     else:
    #         song_cache = os.path.isfile('./data/music_cache/song.mp3')
    #
    #         try:
    #             if song_cache:
    #                 os.remove('./data/music_cache/song.mp3')
    #         except PermissionError:
    #             await ctx.send(f"Wacht todat de muziek gedaan is of gebruik de {prefix}stop command.")
    #             return
    #
    #         voice_channel = get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    #         await voice_channel.connect()
    #         await ctx.send(f"🟢 **De bot is het kanaal** `{voice_channel}` **gejoined!**")
    #
    #         voice = get(self.client.voice_clients, guild=ctx.guild)
    #
    #         ydl_opts = {
    #             'format': 'bestaudio/best',
    #             'postprocessors': [{
    #                 'key': 'FFmpegExtractAudio',
    #                 'preferredcodec': 'mp3',
    #                 'preferredquality': '192'
    #             }]
    #         }
    #
    #         await ctx.send(f"<:youtube:794581601563836447> **Zoeken naar muziek** `{url}`")
    #         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #             ydl.download([url])
    #             info_dict = ydl.extract_info(url, download=False)
    #             video_title = info_dict.get('title', None)
    #
    #         for file in os.listdir('./'):
    #             if file.endswith('.mp3'):
    #                 os.rename(file, 'data/music_cache/song.mp3')
    #
    #         voice.play(discord.FFmpegPCMAudio('data/music_cache/song.mp3'))
    #         await ctx.send(f"🎶 **Speelt nu: ** `{video_title}`")

    @commands.command()
    @commands.is_owner()
    async def loopmusic(self, ctx):
        url = 'https://www.youtube.com/watch?v=LaQj636PJh0'
        song_cache = os.path.isfile('./data/music_cache/loop.mp3')
        doorgaan = False

        try:
            if song_cache:
                doorgaan = True
        except PermissionError:
            await ctx.send(f"Wacht todat de muziek gedaan is of gebruik de {prefix}stop command.")
            return

        voice_channel = get(ctx.guild.voice_channels, id=793975019851218944)
        await voice_channel.connect()
        await ctx.send(f"🟢 **De bot is nu gebonden aan** `{voice_channel}`")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }

        video_title = None
        await ctx.send(f"<:youtube:794581601563836447> **Zoeken naar muziek** `{url}`")
        if not doorgaan:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', None)

            for file in os.listdir('./'):
                if file.endswith('.mp3'):
                    os.rename(file, 'data/music_cache/loop.mp3')

        if video_title is None:
            video_title = 'Best Music Mix ♫ No Copyright EDM ♫ Gaming Music Trap, House, Dubstep'
        await ctx.send(f"🎶 **Loopt nu: ** `{video_title}`")

        def repeat(guild, voice, audio):
            voice.play(audio, after=lambda e: repeat(guild, voice, audio))
            voice.is_playing()

        audio = discord.FFmpegPCMAudio('data/music_cache/loop.mp3')
        voice.play(audio, after=lambda e: repeat(ctx.guild, voice, audio))
        voice.is_playing()

    # @commands.command()
    # async def leave(self, ctx):
    #     voice = get(self.client.voice_clients, guild=ctx.guild)
    #
    #     doorgaan = True
    #     if voice is not None:
    #         if not voice.is_connected():
    #             await ctx.send(f"De bot zit niet in een channel.")
    #             doorgaan = False
    #
    #     if doorgaan:
    #         await voice.disconnect()
    #
    # @commands.command()
    # async def pause(self, ctx):
    #     voice = get(self.client.voice_clients, guild=ctx.guild)
    #
    #     doorgaan = True
    #     if voice is not None:
    #         if not voice.is_playing():
    #             await ctx.send(f"De bot is geen muziek aan het spelen.")
    #             doorgaan = False
    #
    #     if doorgaan:
    #         await voice.pause()
    #
    # @commands.command()
    # async def resume(self, ctx):
    #     voice = get(self.client.voice_clients, guild=ctx.guild)
    #
    #     doorgaan = True
    #     if voice is not None:
    #         if not voice.is_paused():
    #             await ctx.send(f"De bot was niet gepauzeerd.")
    #             doorgaan = False
    #
    #     if doorgaan:
    #         await voice.resume()
    #
    # @commands.command()
    # async def stop(self, ctx):
    #     voice = get(self.client.voice_clients, guild=ctx.guild)
    #
    #     await voice.stop()
    #
    # @commands.command()
    # async def test(self, ctx):
    #     print(ctx.author.voice)


def setup(client):
    client.add_cog(Muziek(client))
