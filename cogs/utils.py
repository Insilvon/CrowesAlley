from discord.ext import commands


class Utils(commands.Cog):
    bot = None
    # Register the cog with
    # await bot.add_cog(Utils(bot))
    def _init_(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")
