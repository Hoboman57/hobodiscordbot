from ast import alias
import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    def search_yt(self, item):
        try:
            if item.startswith("https://"):
                info = self.ytdl.extract_info(item, download=False)
                title = info["title"] if "title" in info else "Unknown Title"
                return {'source': item, 'title': title}
            search = VideosSearch(item, limit=1)
            result = search.result()["result"]
            if not result:
                return False
            return {'source': result[0]["link"], 'title': result[0]["title"]}
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return False

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            voice_channel = self.music_queue[0][1]
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            try:
                data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
                print("yt_dlp data:", data)
                song = data.get('url')
                if song and self.vc and self.vc.is_connected():
                    def after_playing(error):
                        if error:
                            print(f"Player error: {error}")
                        asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)
                    if not self.vc.is_playing():
                        self.vc.play(
                            discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS),
                            after=after_playing
                        )
                else:
                    print("No song URL found or already playing.")
            except Exception as e:
                print(f"Error in play_next: {e}")
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            voice_channel = self.music_queue[0][1]
            try:
                if self.vc is None or not self.vc.is_connected():
                    self.vc = await voice_channel.connect()
                    if self.vc is None:
                        await ctx.send("```Could not connect to the voice channel```")
                        return
                else:
                    await self.vc.move_to(voice_channel)
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
                print("yt_dlp data:", data)
                song = data.get('url')
                if song and not self.vc.is_playing():
                    def after_playing(error):
                        if error:
                            print(f"Player error: {error}")
                        asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)
                    self.vc.play(
                        discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS),
                        after=after_playing
                    )
                else:
                    await ctx.send("```Could not play the song.```")
            except Exception as e:
                await ctx.send(f"Error playing music: {e}")
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel
        except Exception:
            await ctx.send("```You need to connect to a voice channel first!```")
            return
        if self.is_paused:
            try:
                self.vc.resume()
            except Exception as e:
                await ctx.send(f"Error resuming: {e}")
        else:
            song = self.search_yt(query)
            if not song:
                await ctx.send("```Could not download the song. Incorrect format or no results. Try another keyword.```")
            else:
                try:
                    if self.is_playing:
                        await ctx.send(f"**#{len(self.music_queue)+2} -'{song['title']}'** added to the queue")
                    else:
                        await ctx.send(f"**'{song['title']}'** added to the queue")
                    self.music_queue.append([song, voice_channel])
                    if not self.is_playing:
                        await self.play_music(ctx)
                except Exception as e:
                    await ctx.send(f"Error adding song: {e}")

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        try:
            if self.is_playing:
                self.is_playing = False
                self.is_paused = True
                if self.vc and self.vc.is_connected():
                    self.vc.pause()
            elif self.is_paused:
                self.is_paused = False
                self.is_playing = True
                if self.vc and self.vc.is_connected():
                    self.vc.resume()
        except Exception as e:
            await ctx.send(f"Error pausing/resuming: {e}")

    @commands.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        try:
            if self.is_paused:
                self.is_paused = False
                self.is_playing = True
                if self.vc and self.vc.is_connected():
                    self.vc.resume()
        except Exception as e:
            await ctx.send(f"Error resuming: {e}")

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        try:
            if self.vc and self.vc.is_connected():
                self.vc.stop()
                await self.play_music(ctx)
        except Exception as e:
            await ctx.send(f"Error skipping: {e}")

    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        try:
            retval = ""
            for i in range(0, len(self.music_queue)):
                retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"
            if retval != "":
                await ctx.send(f"```queue:\n{retval}```")
            else:
                await ctx.send("```No music in queue```")
        except Exception as e:
            await ctx.send(f"Error displaying queue: {e}")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        try:
            if self.vc and self.vc.is_connected() and self.is_playing:
                self.vc.stop()
            self.music_queue = []
            await ctx.send("```Music queue cleared```")
        except Exception as e:
            await ctx.send(f"Error clearing queue: {e}")

    @commands.command(name="stop", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        try:
            self.is_playing = False
            self.is_paused = False
            if self.vc and self.vc.is_connected():
                await self.vc.disconnect()
            await ctx.send("```Disconnected from voice channel```")
        except Exception as e:
            await ctx.send(f"Error disconnecting: {e}")

    @commands.command(name="remove", help="Removes last song added to queue")
    async def re(self, ctx):
        try:
            if self.music_queue:
                self.music_queue.pop()
                await ctx.send("```last song removed```")
            else:
                await ctx.send("```Queue is already empty```")
        except Exception as e:
            await ctx.send(f"Error removing song: {e}")