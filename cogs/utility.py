#######################################################################################################################################################
#Filename: cog.py                                                                                                                                     #
#Author(s):Jared De Los Santos , Omar Trejo , Charles Morrison                                                                                        #
#Date Last Updated: 9/22/22                                                                                                                           #
#Purpose of File:                                                                                                                                     #
#######################################################################################################################################################

import discord
from discord.ext import commands
from discord import File
from easy_pil import Editor, load_image_async, Font

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
    """Any sort of greeting command or listener event."""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            background = Editor("TDMwelcome.png")
            profile_image = await load_image_async(str(member.avatar.url))

            profile = Editor(profile_image).resize((150, 150)).circle_image()
            poppins = Font.poppins(size=45, variant="bold")

            poppins_small = Font.poppins(size=20, variant="light")

            background.paste(profile, (325, 90))
            background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)

            background.text((400, 260), f"Welcome to {member.guild.name}", color="white", font = poppins, align="center")
            background.text((400, 325), f"{member.name}#{member.discriminator}", color="black", font=poppins_small, align="center")

            file = File(fp=background.image_bytes, filename="TDMwelcome.png")
            await channel.send(file = file)
            await member.send(f'Welcome to {member.guild.name}!, {member.name}! :partying_face:')
        
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello."""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}!')
        else:
            await ctx.send(f"Hello {member.name}... I've said that already!")
        self._last_member = member

class Ping(commands.Cog, name = "Ping"):
    """A check to see if the bot is active."""
    
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
