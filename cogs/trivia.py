#######################################################################################################################################################
#Filename: trivia.py                                                                                                                                  #
#Author(s): Charles Morrison (main author), Jared De Los Santos (cleaner of code)                                                                     #
#Date Last Updated: 11/15/22                                                                                                                          #
#Purpose of File: This file communicates with the Discord API to create a CSUF                                                                        #
#                 computer science based trivia game for Discord servers.                                                                             #
#######################################################################################################################################################


import discord
from discord.ext import commands
import random

# TriviaLoader class is used to load trivia questions from a text file, trivia_list.txt, and store them in a dictionary
class TriviaLoader:
    def __init__(self):
        self.trivia_list = {}
        self.total = 0
        self.current_question = 0

    # open(): Opens trivia_list.txt and stores them in a dictionary (self.trivia_list)
    def open(self):
        trivia_file = open("trivia_list.txt", "r")
        for t_item in trivia_file:
            split_trivia = t_item.split("::")
            trivia_construct = {'question': split_trivia[0],
                                'correct': split_trivia[1],
                                'answers': split_trivia[2].split("+"),
                                'source': split_trivia[3]}
            self.trivia_list[self.total] = trivia_construct
            self.total += 1
        trivia_file.close()

    # get_answer() gets the answer from the discord user and checks to see if the answer is coreect or not.
    # this file also will show the sources for the answers (Works Cited)
    def get_answer(self, answer):
        if self.current_question != 0:
            answer = int(answer)
            correct_answer = self.trivia_list[self.current_question]['correct']
            my_answer = self.trivia_list[self.current_question]['answers'][answer-1]
            source = self.trivia_list[self.current_question]['source']
            self.current_question = 0
            if my_answer == correct_answer:
                return ("Correct!" + "\n\n\nWorks Cited: " + str(source))
            else:
                return ("Incorrect! The Answer is: " + str(correct_answer) + "\n\n\nWorks Cited: " + str(source))


    # generate() will choose a random question from the list of questions and will return the trivia question with a list of options.
    def generate(self):
        rand_num = random.randint(0, (self.total+1))
        while rand_num >= self.total:
            rand_num = random.randint(0, (self.total+1))

        self.current_question = rand_num
        trivia_question = self.trivia_list[rand_num]['question'] + "\n\n"

        answer_num = 1
        for answer in self.trivia_list[rand_num]['answers']:
            trivia_question += (str(answer_num) + ". " + str(answer) + "\n")
            answer_num += 1
        return trivia_question

    # play() is just the instruction manual for the trivia game
    def play(self):
        return "Welcome to CSUF Computer Science Trivia! \n\n How To Play: \n- To Answer Questions: Type the number next to answer (ex: 1. Bob -> Type 1) \n- To Play: Type '.trivia start'"


# Trivia is used to communicate with the Discord API and the TriviaLoader class
class Trivia(commands.Cog, name = "Trivia"):
    """CSUF related trivia fun!"""
    def __init__(self, bot):
        self.bot = bot
        self.trivia = TriviaLoader() # calling TriviaLoader() class
        self.trivia.open() # loading text file data and storing them in dictionary


    #required to have it show up on the help command
    @commands.command()
    async def trivia(self, ctx, word):
        """Command to run the game. Two options for parameter: help or start """
        def check(msg):
            return msg.content == "hello" and msg.channel == ctx.channel
        
        if word == 'help':
            pass
        elif word == 'start':
            # await ctx.channel.send(self.trivia.generate())
            # message = await self.bot.wait_for("message",check=check)
            # await ctx.channel.send(self.trivia.get_answer(answer=ctx.content))
            pass
        else:
            await ctx.send("Invalid parameter. Only help or start.")
            await ctx.send("Ex: .trivia help or .trivia start")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        num_choices = ['1','2','3','4']
        if ctx.content == ".trivia help":
            await ctx.channel.send(self.trivia.play())
        elif ctx.content == ".trivia start":
            await ctx.channel.send(self.trivia.generate())
        elif ctx.content in num_choices:
            await ctx.channel.send(self.trivia.get_answer(answer=ctx.content)) # Process answers
            return
        else:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(Trivia(bot))
