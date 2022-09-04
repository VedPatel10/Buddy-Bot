import discord
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unidecode

class MLB(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def mlb(self, ctx, *, input):
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
    url = "https://www.baseball-reference.com/players/" + first_letter.lower()
    url_p1 = ""
    html = urlopen(url)
    soup = BeautifulSoup(html, "html5lib")
  
    players = soup.find('div', {'id':'div_players_'}).findAll('a')
    
    for i in players:
      compare_to = i.getText()
      if compare_to[-1] == "+":
        compare_to = compare_to[0:-1]
      if unidecode.unidecode(compare_to.lower()) == unidecode.unidecode(player.lower()):
          print("MLB Player: " + compare_to)
          url_p1 = "https://www.baseball-reference.com/" + i.get('href')
          break
  
    if url_p1 != "":
      print(url_p1)
      html_p1 = urlopen(url_p1)
      soup_p1 = BeautifulSoup(html_p1, "html5lib")
      accolades = []
      pitcher = False
  
      if (soup_p1.find('div', {'id':'meta'}).find('p').getText().split()[-1]) == "Pitcher" and len(soup_p1.find('div', {'id':'meta'}).find('p').getText().split()) == 2:
        pitcher = True

      if pitcher == True:
        table_p1 = soup_p1.find("table", {"id":"pitching_standard"})
      else:
        table_p1 = soup_p1.find("table", {"id":"batting_standard"})
      
      if year == "Career":
        row_p1 = table_p1.find("tfoot").find("tr")
        if soup_p1.find('ul', {'id':'bling'}) != None:
          for i in soup_p1.find('ul', {'id':'bling'}).findAll('li'):
            accolades.append(i.getText())
          accolades = '\n'.join(map(str, accolades))
      else:
        if pitcher == True:
          row_p1 = table_p1.find("tbody").find("tr", {"id":"pitching_standard." + year})
        else:
          row_p1 = table_p1.find("tbody").find("tr", {"id":"batting_standard." + year})
  
      if row_p1 is not None:
        embed = discord.Embed(title=compare_to, url=url_p1, color=discord.Color.gold()) 
        gp_p1 = row_p1.find('td', {'data-stat':"G"}).getText()
        year = row_p1.find('th').getText()
        
        if pitcher == True:
          w_p1 = row_p1.find('td', {"data-stat":"W"}).getText()
          l_p1 = row_p1.find('td', {"data-stat":"L"}).getText()
          era_p1 = row_p1.find('td', {"data-stat":"earned_run_avg"}).getText()
          sv_p1 = row_p1.find('td', {"data-stat":"SV"}).getText()
          
          embed.add_field(name=year + ":", value=f'{gp_p1} games \n{w_p1}-{l_p1} \n{era_p1} era \n{sv_p1} saves', inline=True) 
        else:
          h_p1 = row_p1.find('td', {"data-stat":"H"}).getText()
          hr_p1 = row_p1.find('td', {"data-stat":"HR"}).getText()
          rbi_p1 = row_p1.find('td', {"data-stat":"RBI"}).getText()
          ba_p1 = row_p1.find('td', {"data-stat":"batting_avg"}).getText()
          
          embed.add_field(name=year + ":", value=f'{gp_p1} gp \n{h_p1} hits \n{hr_p1} HR \n{rbi_p1} RBI \n{ba_p1} avg', inline=True) 
        
        img = soup_p1.find('div', {'id':'meta'}).find('img').get('src')   
        embed.set_thumbnail(url=img)
        
        if accolades:
          embed.add_field(name="Accolades:", value=accolades, inline=True)
        await ctx.send(embed=embed)
        
        print(f'{compare_to} {year}: {gp_p1} gp')
      else: 
        await ctx.send(compare_to + " did not play in the "+ str(year) + " season")
    else:
      await ctx.send(f'Unable to find {input}')
      print(f'{input} could not be found')
    
    url_p1 = ""
    year = ""
    accolades = []
    print("\n")

def setup(bot):
  bot.add_cog(MLB(bot))