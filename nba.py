import discord
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unidecode

class NBA(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def nba(self, ctx, *, input):
    print("Input: " + input)
    
    year = input.split()[-1]
    if year.isdigit() == True:
      player = input[:-5]
    else:
      if year.lower() == "career":
        input = ' '.join(input.split()[:-1])
      year = "Career"
      player = input
    print("Year: " + year)
    
    first_letter = player.split()[1][0]
    # print(first_letter)
    
    url = "https://www.basketball-reference.com/players/" + first_letter.lower()
    url_p1 = ""
    html = urlopen(url)
    soup = BeautifulSoup(html, "html5lib")
    
    players = soup.find('tbody').findAll('th')
    # print(players)
    
    for i in players:
      compare_to = i.getText()
      if compare_to[-1] == "*":
        compare_to = compare_to[:-1]
      if unidecode.unidecode(compare_to.lower()) == unidecode.unidecode(player.lower()):
          # player = i.getText()
          print("NBA Player: " + compare_to)
          # print(i.getText())
          # a = (soup.find(i).find('a')).find('href')            
          # print(i.find('a').get('href'))
          url_p1 = "https://www.basketball-reference.com/" + i.find('a').get('href')
          break
    
    if url_p1 != "":
      print(url_p1)
      html_p1 = urlopen(url_p1)
      soup_p1 = BeautifulSoup(html_p1, "html5lib")
      accolades = []
  
      table_p1 = soup_p1.find("table", {"id":"per_game"})
      if year == "Career":
        row_p1 = table_p1.find("tfoot").find("tr")
  
        if soup_p1.find('ul', {'id':'bling'}) != None:
          for i in soup_p1.find('ul', {'id':'bling'}).findAll('li'):
            accolades.append(i.getText())
          accolades = '\n'.join(map(str, accolades))
      else:
        row_p1 = table_p1.find("tbody").find("tr", {"id":"per_game." + year})
  
      if row_p1 is not None:
        g_p1 = row_p1.find('td', {'data-stat': "g"}).getText()
        ppg_p1 = row_p1.find('td', {"data-stat" : "pts_per_g"}).getText()
        trb_p1 = row_p1.find('td', {"data-stat" : "trb_per_g"}).getText()
        ast_p1 = row_p1.find('td', {"data-stat" : "ast_per_g"}).getText()
        year = row_p1.find('th', {"data-stat" : "season"}).getText()
        img = soup_p1.find("img", {"itemscope": "image"}).get('src')
  
        embed = discord.Embed(title=compare_to, url=url_p1, color=discord.Color.orange())
        embed.add_field(name=year + ":", value=f'{g_p1} gp \n{ppg_p1} ppg \n{trb_p1} reb \n{ast_p1} ast', inline=True)
        embed.set_thumbnail(url=img)
        
        if accolades:
          embed.add_field(name="Accolades:", value=accolades, inline=True)
        await ctx.send(embed=embed)
        
        print(f'{compare_to} {year}: {ppg_p1} ppg')
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
  bot.add_cog(NBA(bot))