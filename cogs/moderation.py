import discord
from discord.ext import commands

class Moderation(commands.Cog, name = "Moderation"):
    def __init__(self, bot):
        self.bot = bot
    # @commands.Cog.listener()

    #asterisk is sort of like a way to append all the words we write into reason
    #since it is after member, it appends all words after that parameter into reason (for clarification)
    @commands.command()
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if ctx.message.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            embed = discord.Embed(
                color=0xED4245,
                title=f'{member.name}#{member.discriminator} has been kicked. :x:',
                description=f'Reason: {reason}',
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0xED4245,
                title='Permission Denied',
                description=f'You do not have access to this command.',
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)

    @commands.command(name='ban')
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Have to mention the user in order for it to successfully\n
        Can insert reason if needed, but optional:"""
        if ctx.message.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            embed = discord.Embed(
                color=0x992D22,
                title=f'{member.name}#{member.discriminator} has been banned. :hammer:',
                description=f'Reason: {reason}',
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0xED4245,
                title='Permission Denied',
                description=f'You do not have access to this command.',
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)

    """Only useable if you have the user's ID; not possible with their username and discriminator."""
    @commands.command(name='unban')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        
        embed = discord.Embed(
            color=0x57F287,
            title=f'User with id: **{userId}** has been unbanned. :white_check_mark:',
            timestamp=ctx.message.created_at
        )

        await ctx.guild.unban(user)
        await ctx.send(embed=embed)

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                color=0x57F287,
                title=f'Muted user {member.name}#{member.discriminator}.',
                timestamp=ctx.message.created_at
            )
            guild = ctx.guild
            muteRole = discord.utils.get(guild.roles, name = "muted")

            if not muteRole:
                muteRole = await guild.create_role(name = "muted")

                for channel in guild.channels:
                    await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
            await member.add_roles(muteRole, reason=None)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0xED4245,
                title='Permission Denied',
                description=f'You do not have access to this command.',
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                color=0x57F287,
                title=f'Unmuted user {member.name}#{member.discriminator}.',
                timestamp=ctx.message.created_at
            )
            guild = ctx.guild
            muteRole = discord.utils.get(guild.roles, name = "muted")

            if not muteRole:
                muteRole = await guild.create_role(name = "muted")

                for channel in guild.channels:
                    await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
            await member.remove_roles(muteRole, reason=None)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0xED4245,
                title='Permission Denied',
                description=f'You do not have access to this command.',
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)


"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
