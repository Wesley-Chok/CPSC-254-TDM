#######################################################################################################################################################
#Filename: main.py                                                                                                                                    #
#Author(s):Jared De Los Santos , Omar Trejo , Charles Morrison                                                                                        #
#Date Last Updated: 9/22/22                                                                                                                           #
#Purpose of File: Main file that initializes the Bot and will call function that will be features of the bot.                                         #
#######################################################################################################################################################

import discord
from discord.ext import commands

import os 
import dotenv
from dotenv import load_dotenv

def main():
    intents = discord.Intents.default()
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
        # for each subfolder within our directory, "modules"
        # if a path exists for modules/{folder}/cog.py
        # we will load the Cog by doing client.load_extension(f"modules.{folder}.cog")
        #
        # NOTE: LOADING cogs is what gets them to run as a command
        #       There is an automatic built-in help command so, if you
        #       run the bot, and type .help, it shows us all the commands
        #       that we have created. (There should be 3: Greetings, Ping, No Category)
        for folder in os.listdir("modules"):
            if os.path.exists(os.path.join("modules", folder, "cog.py")):
                await client.load_extension(f"modules.{folder}.cog")

    #loads our token from our .env file
    load_dotenv()
    token = os.getenv('TOKEN')

    #runs the token with discord so that the bot can come online.
    client.run(token)

if __name__ == '__main__':
    main()
