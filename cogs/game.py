#######################################################################################################################################################
#Filename: game.py                                                                                                                                    #
#Author(s): Jared De Los Santos                                                                                                                       #
#Date Last Updated: 11/15/22                                                                                                                          #
#Purpose of File: Has minigames that involve player vs bot and player vs player.                                                                      #
#######################################################################################################################################################

import discord
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
import random

from typing import List

#test for now using buttons

class Game(commands.Cog, name = "Game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, user_choice=None):
        """Start RPS with a bot."""
        rpsGame = ['rock', 'paper', 'scissors']
        if user_choice is None or user_choice == '':
            await ctx.send("> You need to pass in rock, paper, or scissors!")
        else:
            if user_choice.lower() in rpsGame: 
                bot_choice = random.choice(rpsGame)
                await ctx.send(f"{ctx.author.name}'s choice: `{user_choice}`\nMy choice: `{bot_choice}`")
                user_choice = user_choice.lower() 
                if user_choice == bot_choice:
                    await ctx.send("Chose the same one. You're lucky. Let's go again.")

                # Rock Win Conditions #
                if user_choice == 'rock' and bot_choice == 'paper':
                    await ctx.send('I won! Too easy.')
                if user_choice == 'rock' and bot_choice == 'scissors':
                    await ctx.send('You won...')

                # Paper Win Conditions #
                if user_choice == 'paper' and bot_choice == 'rock':
                    await ctx.send('You won...')
                if user_choice == 'paper' and bot_choice == 'scissors':
                    await ctx.send("I won! That won't work on me!")

                # Scissor Win Conditions #
                if user_choice == 'scissors' and bot_choice == 'paper':
                    await ctx.send('You won...')
                if user_choice == 'scissors' and bot_choice == 'rock':
                    await ctx.send('I won! Better luck next time.')
            else:
                await ctx.send('> Invalid argument.')

    @commands.command()
    #ctx: commands.Context
    async def ttt(self, ctx, opp: discord.Member):
        """Start a tictactoe game with another player."""
        if ctx.author == opp:
            await ctx.send(f"Nice try, {ctx.author.mention}... but you cannot challenge yourself.")
            return
        if opp.bot:
            await ctx.send(f"{ctx.author.mention}, you'd embarass yourself trying to verse one of us.")
            return

        global player1
        global player2

        player1 = ctx.author
        player2 = opp

        await ctx.send(f"Tic Tac Toe: {ctx.author.mention} is X, {opp.mention} is O", view=TTT())

class TTTButton(discord.ui.Button["TTT"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed.
    # This is part of the "meat" of the game logic.
    async def callback(self, interaction: discord.Interaction):
        #assert throws exception if self.view IS none
        global player1
        global player2

        assert self.view is not None

        #sets the view to our graphical tictactoe class
        view: TTT = self.view

        state = view.board[self.y][self.x]

        #doesn't allow us to click on already clicked spots
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            #danger is red
            if interaction.user != player1:
                await interaction.response.send_message(f"It's {player1.name}'s turn", ephemeral=True)
            else:
                self.style = discord.ButtonStyle.danger
                self.label = "X"
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.O
                content = "It is now O's turn"
        else:
            #success is green
            if interaction.user != player2:
                await interaction.response.send_message(f"It's {player2.name}'s turn", ephemeral=True)
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


#represents the graphical view for our board
class TTT(discord.ui.View):
    children: List[TTTButton]

    #we give these variables value so that we can determine who wins
    X = -1
    O = 1
    TIE = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        #we add to our graphical ui the button
        #double for loop since tictactoe is 3x3
        for x in range(3):
            for y in range(3):
                self.add_item(TTTButton(x, y))

    # helps check who is winning and this gets used by TTTButton
    def check_board_winner(self):

        #checks for any horizontal match
        for horizontal in self.board:
            value = sum(horizontal)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # vertical match
        for vertical in range(3):
            value = self.board[0][vertical] + self.board[1][vertical] + self.board[2][vertical]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # diagonal match
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        #other diag match
        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        # if no matches our last case is a tie
        if all(i != 0 for row in self.board for i in row):
            return self.TIE

        return None
            

"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(Game(bot))