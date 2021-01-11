from discord.ext import commands


class CommandsConverters(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='python', aliases=['py'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _python(self, ctx, *, programma: str):
        valid_channels = ['👾│geek-chat', '💻│programmeren']

        if str(ctx.channel) in valid_channels:
            await ctx.message.delete()

            if len(programma) <= 1900:
                await ctx.send(f"**Code Snippet van {ctx.author}**\n```py\n{programma}\n```")
            else:
                await ctx.send("Je programma is te lang...")

    @commands.command(name='javascript', aliases=['js'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _javascript(self, ctx, *, programma: str):
        valid_channels = ['👾│geek-chat', '💻│programmeren']

        if str(ctx.channel) in valid_channels:
            await ctx.message.delete()

            if len(programma) <= 1900:
                await ctx.send(f"**Code Snippet van {ctx.author}**\n```js\n{programma}\n```")
            else:
                await ctx.send("Je programma is te lang...")

    @commands.command(name='css')
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _css(self, ctx, *, programma: str):
        valid_channels = ['👾│geek-chat', '💻│programmeren']

        if str(ctx.channel) in valid_channels:
            await ctx.message.delete()

            if len(programma) <= 1900:
                await ctx.send(f"**Code Snippet van {ctx.author}**\n```css\n{programma}\n```")
            else:
                await ctx.send("Je programma is te lang...")

    @commands.command(name='html')
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _html(self, ctx, *, programma: str):
        valid_channels = ['👾│geek-chat', '💻│programmeren']

        if str(ctx.channel) in valid_channels:
            await ctx.message.delete()

            if len(programma) <= 1900:
                await ctx.send(f"**Code Snippet van {ctx.author}**\n```html\n{programma}\n```")
            else:
                await ctx.send("Je programma is te lang...")

    @commands.command(name='markdown', aliases=['md'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _markdown(self, ctx, *, programma: str):
        valid_channels = ['👾│geek-chat', '💻│programmeren']

        if str(ctx.channel) in valid_channels:
            await ctx.message.delete()

            if len(programma) <= 1900:
                await ctx.send(f"**Code Snippet van {ctx.author}**\n```md\n{programma}\n```")
            else:
                await ctx.send("Je programma is te lang...")

    @commands.command(name='cpp', aliases=['c++', 'cplusplus'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _cpp(self, ctx, *, programma: str):
        valid_channels = ['👾│geek-chat', '💻│programmeren']

        if str(ctx.channel) in valid_channels:
            await ctx.message.delete()

            if len(programma) <= 1900:
                await ctx.send(f"**Code Snippet van {ctx.author}**\n```c++\n{programma}\n```")
            else:
                await ctx.send("Je programma is te lang...")


def setup(client):
    client.add_cog(CommandsConverters(client))
