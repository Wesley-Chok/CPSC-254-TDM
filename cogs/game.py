import discord
from discord.ui import Button, View
from discord.ext import commands

#test for now using buttons

class Game(commands.Cog, name = "Game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx):
        rock = Button(label="Rock", style=discord.ButtonStyle.primary, emoji ="🪨")
        paper = Button(label="Paper", style=discord.ButtonStyle.primary, emoji ="📃")
        scissors = Button(label="Scissors", style=discord.ButtonStyle.primary, emoji ="✂")

        async def button_callback(interaction):
            await interaction.response.edit_message(content = f'{ctx.author.name} has chosen an option.')

        rock.callback = button_callback
        paper.callback = button_callback
        scissors.callback = button_callback

        view = View()
        view.add_item(rock)
        view.add_item(paper)
        view.add_item(scissors)
        #view.remove_item()
        await ctx.send(f'{ctx.author.mention}', view=view)
        

"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(Game(bot))