import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO


class OnJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        join_channel = self.client.get_channel(793979727806332959)

        stats_channel = self.client.get_channel(793983008641253416)
        guild_ids = stats_channel.guild

        welcome_photo = Image.open('data/welcome_template.png')
        font = ImageFont.truetype('data/roboto.ttf', 43)

        draw = ImageDraw.Draw(welcome_photo)
        text = f"{member} is gejoined!"
        members_text = f"Speler: #{guild_ids.member_count}"

        max_lengte, max_hoogte = 1100, 500

        w, h = draw.textsize(text, font=font)
        draw.text(((max_lengte - w) / 2, 298), text, (255, 255, 255), font=font)

        w2, h2 = draw.textsize(members_text, font=font)
        draw.text(((max_lengte - w2) / 2, 363), members_text, (95, 95, 95), font=font)

        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((170, 170))

        welcome_photo.paste(pfp, (465, 93))
        welcome_photo.save('data/profile.png')

        await join_channel.send(file=discord.File('data/profile.png'))
        await stats_channel.edit(name=f"✨ Members: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnJoin(client))
