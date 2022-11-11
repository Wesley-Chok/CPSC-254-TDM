#######################################################################################################################################################
#Filename: main.py                                                                                                                                    #
#Author(s):Jared De Los Santos , Omar Trejo , Charles Morrison                                                                                        #
#Date Last Updated: 9/22/22                                                                                                                           #
#Purpose of File: Main file that initializes the Bot and will call function that will be features of the bot.                                         #
#######################################################################################################################################################

import discord
from discord.ext import commands
from discord import File
from easy_pil import Editor, load_image_async, Font

import os 
from dotenv import load_dotenv

def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    #Our connection to Discord.
    # client = discord.Client(intents=intents)
    # our bot prefix will be . (so for example: .help)
    # we will be using Cogs to sort most of the commands that we can do
    # check cog.py under modules/utility
    client = commands.Bot(command_prefix=".", intents=intents)

    #client.event() REGISTERS an event.
    """on_ready gets called whenever the bot has finished logging in
    and setting things up."""
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        # NOTE: LOADING cogs is what gets them to run as a command
        #       There is an automatic built-in help command so, if you
        #       run the bot, and type .help, it shows us all the commands
        #       that we have created.
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                await client.load_extension(f"cogs.{filename[:-3]}")

    @client.command(name='load', hidden = True)
    # @commands.is_owner()
    async def load(ctx, extension):
        await client.load_extension(f'cogs.{extension}')
        embed = discord.Embed(
            title = f'Loaded cog: **{extension}**',
            color = 0xff00c8,
            timestamp = ctx.message.created_at
        )

        await ctx.send(embed=embed)

    @client.command(name='unload', hidden = True)
    # @commands.is_owner()
    async def unload(ctx, extension):
        await client.unload_extension(f'cogs.{extension}')
        embed = discord.Embed(
            title = f'Unloaded cog: **{extension}**',
            color = 0xff00c8,
            timestamp = ctx.message.created_at
        )

        await ctx.send(embed=embed)

    @client.command(name='reload', hidden = True)
    # @commands.is_owner()
    async def reload(ctx):
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                await client.unload_extension(f"cogs.{filename[:-3]}")
                await client.load_extension(f"cogs.{filename[:-3]}")
        
        embed = discord.Embed(
            title = 'Reloaded all cogs!',
            color = 0xff00c8,
            timestamp = ctx.message.created_at
        )

        await ctx.send(embed=embed)

    #loads our token from our .env file
    load_dotenv()
    token = os.getenv('TOKEN')

    #runs the token with discord so that the bot can come online.
    client.run(token)

if __name__ == '__main__':
    main()
