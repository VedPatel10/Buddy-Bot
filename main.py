import os
import discord
from discord.ext import commands
import neverSleep
# neverSleep.awake("https://Buddy2.vedpatel101.repl.co", True)
neverSleep.awake(f"https://{str(os.environ['REPL_SLUG']).lower()}.{str(os.environ['REPL_OWNER']).lower()}.repl.co", True)
import sys

import music, nhl, nba, mlb
cogs = [music, nhl, nba, mlb]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')

for i in range(len(cogs)):
  cogs[i].setup(bot)  
  
# -----------------------------------------------
@bot.event
async def on_ready():
  print("We have logged in as " + bot.user.name)

# ----------------HELLO-------------------------------
@bot.command()
async def hello(ctx, *, input=''):
  await ctx.send("shut up " + ctx.message.author.mention)
  
# ----------------HELP GROUP-------------------------------
@bot.group(invoke_without_command=True)
async def help(ctx):
  embed = discord.Embed(title="Help", description="Use !help <command> for more information about a command", color = discord.Color.green())
  embed.add_field(name="Music", value="play, skip, search, pause, resume, join, leave")
  embed.add_field(name="Sports", value="nba, nhl, mlb")
  await ctx.send(embed=embed)
  
# ----------------HELP PLAY-------------------------------
@help.command()
async def play(ctx):
  embed = discord.Embed(title="Play", description="Joins user's voice channel if not already in one and plays YouTube video", color=discord.Color.red())
  embed.add_field(name="Syntax", value = "!play <YouTube video url>")
  await ctx.send(embed=embed)
  
# ----------------HELP SKIP-------------------------------
@help.command()
async def skip(ctx):
  embed = discord.Embed(title="Skip", description="Skips the video that is currently being played", color=discord.Color.red())
  embed.add_field(name="Syntax", value = "!skip")
  await ctx.send(embed=embed)
  
# ----------------HELP SEARCH------------------------------- 
@help.command()
async def search(ctx):
  embed = discord.Embed(title="Search", description="Searches YouTube and returns the top 5 results, which can be played by typing ! + the number of the video", color=discord.Color.red())
  embed.add_field(name="Syntax", value = "!search <whatever you want to search on YouTube>")
  await ctx.send(embed=embed)
  
# ----------------HELP PAUSE-------------------------------
@help.command()
async def pause(ctx):
  embed = discord.Embed(title="Pause", description="Pauses the audio that the bot is playing", color=discord.Color.red())
  embed.add_field(name="Syntax", value = "!pause")
  await ctx.send(embed=embed)
  
# ----------------HELP RESUME-------------------------------
@help.command()
async def resume(ctx):
  embed = discord.Embed(title="Resume", description="Resumes the audio that the bot is playing", color=discord.Color.red())
  embed.add_field(name="Syntax", value = "!resume")
  await ctx.send(embed=embed)
  
# ----------------HELP JOIN-------------------------------
@help.command()
async def join(ctx):
  embed = discord.Embed(title="Join", description="Joins the voice channel of the user if they are in one", color=discord.Color.gold())
  embed.add_field(name="Syntax", value = "!join")
  await ctx.send(embed=embed)
  
# ----------------HELP LEAVE-------------------------------
@help.command()
async def leave(ctx):
  embed = discord.Embed(title="Leave", description="Makes the bot leave the voice channel it is in", color=discord.Color.red())
  embed.add_field(name="Syntax", value = "!leave")
  await ctx.send(embed=embed)
  
# ----------------HELP NBA-------------------------------
@help.command()
async def nba(ctx):
  embed = discord.Embed(title="Nba", description="Brings up NBA player's stats for either a specified season or their entire career", color=discord.Color.orange())
  embed.add_field(name="Syntax", value = "!nba <player's full name> <year (optional)>")
  await ctx.send(embed=embed)
  
# ----------------HELP NHL-------------------------------
@help.command()
async def nhl(ctx):
  embed = discord.Embed(title="Nhl", description="Brings up Nhl player's stats for either a specified season or their entire career", color=discord.Color.blurple())
  embed.add_field(name="Syntax", value = "!nhl <player's full name> <year (optional)>")
  await ctx.send(embed=embed)

# ----------------HELP MLB-------------------------------
@help.command()
async def mlb(ctx):
  embed = discord.Embed(title="Mlb", description="Brings up Mlb player's stats for either a specified season or their entire career", color=discord.Color.gold())
  embed.add_field(name="Syntax", value = "!mlb <player's full name> <year (optional)>")
  await ctx.send(embed=embed)
  
# --------------------------------------------------------
my_secret = os.environ['env']
try:
  bot.run(my_secret)
except:
  os.system("kill 1")
  os.execv(sys.argv[0], sys.argv)
