import discord
from discord.ui import Button, View
from discord.ext import commands

from typing import List

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

    @commands.command()
    async def ttt(self, ctx: commands.Context, user: discord.Member):
        """Starts a tic-tac-toe game with yourself."""
        if ctx.author == user:
            await ctx.send(f"Nice try, {ctx.author.mention}... but you cannot challenge yourself.")
            return
        if user.bot:
            await ctx.send(f"{ctx.author.mention}, you'd embarass yourself trying to verse one of us.")
            return

        await ctx.send("Tic Tac Toe: X goes first", view=TTT(), reference=ctx.message)

    

class TTTButton(discord.ui.Button["TTT"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed.
    # This is part of the "meat" of the game logic.
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TTT = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
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
    Tie = 2

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
            return self.Tie

        return None


    # async def ttt(self, ctx, user: discord.Member):

    #     if ctx.author == user:
    #         await ctx.send(f"{ctx.author.mention}... Now why on god's earth would you challenge yourself?")
    #         return
    #     if user.bot:
    #         await ctx.send(f"{ctx.author.mention} You can't challenge me! You'd lose.")
    #         return

    #     components = [
    #         [Button(style=discord.ButtonStyle.gray,label=str(idx_2+idx)) for idx_2 in range(3)] for idx in range(1,9,3)
    #     ]


            

"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(Game(bot))