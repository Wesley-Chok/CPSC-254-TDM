import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class Music(commands.Cog, name = "Music"):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        #queue will always be empty when the bot starts
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        #giving youtube_dl the options in our YDL_OPTIONS dict
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
                # for i in info:
                #     print(i)
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):

        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            m_title = self.music_queue[0][0]['title']

            info = (YoutubeDL(self.YDL_OPTIONS)).extract_info(m_url, download=False)
            video_id = info.get('webpage_url', None)
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            embed=discord.Embed(title='**Now Playing**', description=f'{m_title}', color=discord.Color.red())

            # for i in info:
            #     print(f'{i}: {info[i]}')
            await ctx.send(embed=embed)
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx) 

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send('**Music is paused.**')
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send('**Music is unpaused.**')

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send('**Music is resumed.**')
        elif self.is_playing:
            await ctx.send('**Music is already playing!**')

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await ctx.send('**Skipped song**')
            await self.play_music(ctx)


    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 10 songs in the current queue
            if (i > 9): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
    
            embed=discord.Embed(title='**Queue**', description='__Songs in the queue__', color=discord.Color.yellow())
            for i in range(0, len(self.music_queue)):
                embed.add_field(name=f"{i+1}. **{self.music_queue[i][0]['title']}**", value='\u200b', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**There is currently no music in queue...**")

    @commands.command(name="clear", aliases=["c"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music stopped and queue cleared.")

    @commands.command(name="leave", aliases=["disconnect", "l", "dc"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await ctx.send("**Leaving voice channel... :wave:**")
        await self.vc.disconnect()

"""setup lets us add a cog to our bot, so that we can load the cog later"""
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
