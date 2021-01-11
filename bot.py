import asyncio
import os
import discord
from discord.ext import commands
from settings import token, botname, folder_list, prefix

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
client.remove_command("help")


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        status = discord.Activity(name=f"Coming Soon", type=discord.ActivityType.playing)
        await client.change_presence(activity=status)
        await asyncio.sleep(300)

for folder in folder_list:
    print(f"[{botname}] ----------------------[ {folder.title()} ]--------------------")
    for filename in os.listdir(f'./{folder}'):
        if filename.endswith('.py'):
            print(f"[{botname}] {folder.title()} > {filename[:-3]} > Loaded!")
            client.load_extension(f'{folder}.{filename[:-3]}')
print(f"[{botname}] ------------------------------------------------------")

client.loop.create_task(change_status())
client.run(token)
