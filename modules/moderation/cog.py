import discord
from discord.ext import commands

class Kick(commands.Cog, name = "Kick"):
    def __init__(self,bot):
        pass
    # @commands.Cog.listener()
    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        pass

"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))
