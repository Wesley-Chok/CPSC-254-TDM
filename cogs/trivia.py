# Name: Charles Morrison
# Date: 11.15.2022
# Description: This file communicates with the Discord API to create a CSUF computer science based trivia game for Discord servers

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
        return "Welcome to CSUF Computer Science Trivia! \n\n How To Play: \n- To Answer Questions: Type the number next to answer (ex: 1. Bob -> Type 1) \n- To Play: Type 'start trivia'"


# Trivia is used to communicate with the Discord API and the TriviaLoader class
class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.trivia = TriviaLoader() # calling TriviaLoader() class
        self.trivia.open() # loading text file data and storing them in dictionary


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "play trivia":
            await message.channel.send(self.trivia.play())
        elif message.content == "start trivia":
            await message.channel.send(self.trivia.generate())
        else:
            await message.channel.send(self.trivia.get_answer(answer=message.content)) # Process answers
        await self.client.process_commands(message)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

async def setup(client):
    await client.add_cog(Trivia(client))
