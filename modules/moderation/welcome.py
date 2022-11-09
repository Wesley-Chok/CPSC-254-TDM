
import discord
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font

bot = commands.Bot(command_prefix='.', intents = discord.Intents.all())

@bot.event
async def on_member_join(member):

    channel = member.guild.system_channel

    background = Editor("pic3.jpg")
    profile_image = await load_image_async(str(member.avatar.url))

    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=50, variant="bold")

    poppins_small = Font.poppins(size=20, variant="light")

    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, ouline="white", stroke_width=5)

    background.text((400, 260), f"Welcome {member.guild.name}", color="white",stroke_width=5)
    background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")

    file = File(fp=background.image_bytes, filename="pic1.jpg")
    await channel.send(f"Hello {member.mention}! Welcome to **{member.guild.name}**")
    await channel.send()
