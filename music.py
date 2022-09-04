import discord
from discord.ext import commands
import youtube_dl
from youtubesearchpython import VideosSearch

# -----------------------------------------------------------
class Music(commands.Cog):
  def _init_(self, bot):  
    self.bot = bot
    
# ------------------------JOIN-------------------------------
  @commands.command(name="join")
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("You are not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)
    print("Joined " + str(voice_channel) + " in " + str(ctx.guild))

# ------------------------LEAVE---------------------------------
  @commands.command()
  async def leave(self, ctx):
    print("Left " + str(ctx.voice_client.channel) + " in " + str(ctx.guild))
    await ctx.voice_client.disconnect()

# ------------------------PLAY-------------------------------
  @commands.command(name="play")
  async def play(self, ctx, url):

    # if ctx.author.voice is None:
    #   await ctx.send("You are not in a voice channel")
    # voice_channel = ctx.author.voice.channel
    # if ctx.voice_client is None:
    #   await voice_channel.connect()
    # else:
    #   await ctx.voice_client.move_to(voice_channel)

    join = ctx.bot.get_command('join')
    await ctx.invoke(join)
    
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    YDL_OPTIONS = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]'}
    # old ydl options: {'format':"bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(source)
      
      print("Now playing " + url + " in " + str(ctx.author.voice.channel) + " in " + str(ctx.guild))

# ------------------------PAUSE-------------------------------
  @commands.command(name="pause")
  async def pause(self, ctx):
    if ctx.voice_client.is_playing() == True:
      ctx.voice_client.pause()
      await ctx.send("Paused")
      print("Paused")
    else:
      await ctx.send("No audio is playing")

# -----------------------RESUME-----------------------------
  @commands.command(name="resume")
  async def resume(self, ctx):
    ctx.voice_client.resume()
    await ctx.send("Resumed")
    print("Resumed")

# ------------------------SKIP------------------------------
  @commands.command(name="skip")
  async def skip(self, ctx):
    if ctx.voice_client.is_playing() == True:
      ctx.voice_client.stop()
      await ctx.send("Skipped")
      print("Skipped")

# ----------------------SEARCH---------------------------------
  @commands.group(name="search", invoke_without_command=True)
  async def search(self, ctx, *, input):
    
    list = 5
    embed = discord.Embed(color=discord.Color.red(), title="YouTube Search - Type ! + # to play a video")
    
    videosSearch = VideosSearch(input, limit = list, language = 'en', region = 'US')
    dict = videosSearch.result()

    global urls
    urls=[]
    urls.clear()
    for i in range(list):
      title = dict['result'][i]['title']
      channel = dict['result'][i]['channel']['name']
      duration = dict['result'][i]['duration']
      date = dict['result'][i]['publishedTime']
      views = dict['result'][i]['viewCount']['text']
      url = dict['result'][i]['link']
      urls.append(url)
      thumbnail = dict['result'][0]['thumbnails'][0]['url']
      embed.add_field(name="!"+str(i+1), inline=True, value=f'{title}\n{url}\n{channel}\n{duration}\n{date}\n{views}\n')
      embed.set_thumbnail(url=thumbnail)
    await ctx.send(embed=embed)

# -----------------------PLAY SEARCH----------------------------
  @commands.command(name='1')
  async def search_1(self, ctx):
    c = ctx.bot.get_command('play')
    await ctx.invoke(c, url=urls[0])

  @commands.command(name='2')
  async def search_2(self, ctx):
    c = ctx.bot.get_command('play')
    await ctx.invoke(c, url=urls[1])

  @commands.command(name='3')
  async def search_3(self, ctx):
    c = ctx.bot.get_command('play')
    await ctx.invoke(c, url=urls[2])

  @commands.command(name='4')
  async def search_4(self, ctx):
    c = ctx.bot.get_command('play')
    await ctx.invoke(c, url=urls[3])

  @commands.command(name='5')
  async def search_5(self, ctx):
    c = ctx.bot.get_command('play')
    await ctx.invoke(c, url=urls[4])
    
# -----------------------------------------------------------
def setup(bot):
  bot.add_cog(Music(bot))