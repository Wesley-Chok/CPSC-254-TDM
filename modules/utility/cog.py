#######################################################################################################################################################
#Filename: cog.py                                                                                                                                     #
#Author(s):Jared De Los Santos , Omar Trejo , Charles Morrison                                                                                        #
#Date Last Updated: 9/22/22                                                                                                                           #
#Purpose of File:                                                                                                                                     #
#######################################################################################################################################################

import discord
from discord.ext import commands

# Modules is the folder where we will store each subclass type
# of things we need to do. Example given: utility. Any utility
# classes/commands we want to add, we would add here. If we decide
# to create another subclass, such as "Fun", we would store any of
# the classes/commands related to the category of "fun".
#
# EACH subclass will have its own cog.py file!
# a video that helped me understand better:
# https://www.youtube.com/watch?v=rgS_OOA12NA

class Greetings(commands.Cog, name = "Greetings"):
    """Any sort of greeting command."""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')
    
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}!')
        else:
            await ctx.send(f"Hello {member.name}... You've been here before")
        self._last_member = member

class Ping(commands.Cog, name = "Ping"):
    """Receives ping commands."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Checks for a response from the bot"""
        await ctx.send("Pong")

"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(Greetings(bot))
    await bot.add_cog(Ping(bot))
