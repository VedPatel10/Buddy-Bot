import discord
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unidecode

class NHL(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def nhl(self, ctx, *, input):
    print("Input: " + input)
    
    year = input.split()[-1]
    if year.isdigit() == True:
      player = input[:-5]
    else:
      if year.lower() == "career":
        input = ' '.join(input.split()[:-1])
      year = "Career"
      player = input
    
    first_letter = player.split()[1][0]
    url = "https://www.hockey-reference.com/players/" + first_letter.lower()
    url_p1 = ""
    html = urlopen(url)
    soup = BeautifulSoup(html, "html5lib")
  
    players = soup.find('div', {'id':'div_players'}).findAll('a')
    
    for i in players:
      compare_to = i.getText()
      if compare_to[-1] == "*":
        compare_to = compare_to[0:-1]
      if unidecode.unidecode(compare_to.lower()) == unidecode.unidecode(player.lower()):
          print("NHL Player: " + compare_to)
          url_p1 = "https://www.hockey-reference.com/" + i.get('href')
          break
  
    if url_p1 != "":
      print(url_p1)
      html_p1 = urlopen(url_p1)
      soup_p1 = BeautifulSoup(html_p1, "html5lib")
      accolades = []
      goalie = False

      if (soup_p1.find('div', {'id':'meta'}).find('p').getText().split()[1]) == "G":
        goalie = True
      
      table_p1 = soup_p1.find("table", {"id":"stats_basic_plus_nhl"})
      if table_p1 is None:
        table_p1 = soup_p1.find("table", {"id":"stats_basic_nhl"})
      if year == "Career":
        foot = table_p1.find("tfoot")
  
        for i in foot:
          try: 
            temp = i.find('th').getText()
          except Exception:
            pass
          if temp == "Career":
            row_p1 = i
            break
        
        if soup_p1.find('ul', {'id':'bling'}) != None:
          for i in soup_p1.find('ul', {'id':'bling'}).findAll('li'):
            accolades.append(i.getText())
          accolades = '\n'.join(map(str, accolades))
      else:
        row_p1 = table_p1.find("tbody").find("tr", {"id":"stats_basic_plus_nhl." + year})
        if row_p1 is None:
          row_p1 = table_p1.find("tbody").find("tr", {"id":"stats_basic_nhl." + year})
      if row_p1 is not None:
        year = row_p1.find('th', {"data-stat" : "season"}).getText()
        embed = discord.Embed(title=compare_to, url=url_p1, color=discord.Color.blurple())
        
        if goalie == True:
          gp_p1 = row_p1.find('td', {'data-stat': "games_goalie"}).getText()
          w_p1 = row_p1.find('td', {'data-stat': "wins_goalie"}).getText()
          l_p1 = row_p1.find('td', {'data-stat': "losses_goalie"}).getText()
          otl_p1 = row_p1.find('td', {'data-stat': "ties_goalie"}).getText()
          svp_p1 = row_p1.find('td', {'data-stat': "save_pct"}).getText()
          gaa_p1 = row_p1.find('td', {'data-stat': "goals_against_avg"}).getText()
          
          embed.add_field(name=year + ":", value=f'{gp_p1} starts \n{w_p1}-{l_p1}-{otl_p1} \n{svp_p1} sv% \n{gaa_p1} gaa', inline=True)
        else:
          gp_p1 = row_p1.find('td', {'data-stat': "games_played"}).getText()
          pts_p1 = row_p1.find('td', {"data-stat" : "points"}).getText()
          g_p1 = row_p1.find('td', {"data-stat" : "goals"}).getText()
          ast_p1 = row_p1.find('td', {"data-stat" : "assists"}).getText()
          
          embed.add_field(name=year + ":", value=f'{gp_p1} gp \n{g_p1} goals \n{ast_p1} assists \n{pts_p1} points', inline=True)
                
        img = soup_p1.find("img", {"itemscope": "image"}).get('src')
        embed.set_thumbnail(url=img)
  
        if accolades:
          embed.add_field(name="Accolades:", value=accolades, inline=True)
        await ctx.send(embed=embed)
        
        print(f'{compare_to} {year}: {gp_p1} gp')
      else: 
        await ctx.send(compare_to + " did not play in the "+ str(int(year)-1) + "-" + year + " season")
    else:
      await ctx.send(f'Unable to find {input}')
      print(f'{input} could not be found')
    
    url_p1 = ""
    year = ""
    accolades = []
    print("\n")

def setup(bot):
  bot.add_cog(NHL(bot))