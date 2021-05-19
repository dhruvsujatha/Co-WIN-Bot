import discord
from discord.ext import commands
import apirequest as ap
import os
import json
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import pytz

PREFIX = 'co@'
IST = pytz.timezone('Asia/Kolkata')

meta = ap.metaAPI()
co = ap.CoWinAPI()
bot = commands.Bot(command_prefix=PREFIX, help_command = None)

def make_app_embed(data, c):
  embed = discord.Embed(title="Appoinments: ", description="Here is a list of available appoinments", color=0x02fa5d, timestamp = datetime.now(IST))   
  embed.set_author(name='We are in this together! Stay Strong!')
  embed.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')
  if c > 2:
    embed.set_footer(text='Data pulled from Co-WIN Public API\nBot made by DhruvS#7149\nLive data updated at')
  else:
    embed.set_footer(text='Bot made by DhruvS#7149\nLive data updated at')
  embed.add_field(name='Name', value=data["name"] ,inline=False)
  embed.add_field(name='Area', value=data["block_name"] ,inline=False)
  embed.add_field(name='Pincode', value=data["pincode"], inline=False)
  embed.add_field(name='Vaccine', value=data["vaccine"] ,inline=False)
  embed.add_field(name='Age Group', value="18 - 45" ,inline=False)
  embed.add_field(name='Date', value=data["date"] ,inline=False)
  embed.add_field(name='Slot Available Time', value=data["from"]+" to "+data["to"] ,inline=False)
  embed.add_field(name='Fee Type', value=data["fee_type"] ,inline=False)
  embed.add_field(name='No of Vaccines available ', value=data["available_capacity"] ,inline=False)
  return embed

@bot.event
async def on_ready():
  activity = discord.Activity(name='co@help | Get Vaccinated!', type=discord.ActivityType.watching)
  await bot.change_presence(activity=activity)
  print('We have logged in as {0.user}'.format(bot))


@bot.command()  
async def test(ctx):
  await ctx.channel.send("```Tested Positive! Wait No....```")

@bot.command()
async def help(ctx):
  embed = discord.Embed(title="Co-WIN Notifier Bot Help", description="Here is a list of available commands", color=0x02fa5d, timestamp = datetime.now(IST))
  embed.set_author(name='We are in this together! Stay Strong!')
  embed.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')

  helpmsg = "\n**Help Message: ** (This one) ```co@help```\n"
  helpmsg += "**Find your State: ** ```co@states``` Remember to note down your State ID.\n\n"
  helpmsg += "**Find your District: ** ```co@dist``` Remember to note down your District ID\n\n"
  helpmsg += "**Find Avaliable Appoinments: ** ```co@appoinments <district_id> <age>"

  embed.add_field(name = '**Commands: **', value = helpmsg)
  embed.set_footer(text = 'That is all Folks!\nBot made by DhruvS#7149\nUpdated at')

  await ctx.channel.send(embed = embed)

@bot.command()
async def states(ctx):
  resp = meta.getstates()
  data = json.loads(resp.text)
  embed = discord.Embed(title="States:", description="Here is a list of available states", color=0x02fa5d, timestamp = datetime.now(IST))
  embed2 = discord.Embed(title="States:", description="Here is a list of available states", color=0x02fa5d, timestamp = datetime.now(IST))
  embed.set_author(name='We are in this together! Stay Strong!')
  embed2.set_author(name='We are in this together! Stay Strong!')
  embed.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')
  embed2.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')
  embed .set_footer(text='That is all Folks!\nChoose the corresponding State ID.\nBot made by DhruvS#7149\nUpdated at')
  embed2 .set_footer(text='That is all Folks!\nChoose the corresponding State ID.\nBot made by DhruvS#7149\nUpdated at')
  for i in range(0, len(data['states'])):
    if i < 18:
      embed.add_field(name = data['states'][i]['state_name'], value = 'State ID: ' + str(data['states'][i]['state_id']))
    else:
      embed2.add_field(name = data['states'][i]['state_name'], value = 'State ID: ' + str(data['states'][i]['state_id']))
  await ctx.channel.send(embed = embed)
  await ctx.channel.send(embed = embed2)

@bot.command()
async def districts(ctx, state_id):
  a, b, c = False, False, False
  resp = meta.getdist(state_id = state_id)
  data = json.loads(resp.text)
  if len(data['districts']) <= 25:
    a = True

  elif len(data['districts']) <= 50:
    a = True
    b = True
  
  else:
    a = True
    b = True
    c = True

  if a:
    embed = discord.Embed(title="Districts:", description="Here is a list of available districts", color=0x02fa5d, timestamp = datetime.now(IST))
    embed.set_author(name = 'We are in this together! Stay Strong!')
    embed.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')
    embed.set_footer(text='That is all Folks!\nChoose the corresponding District ID.\nBot made by DhruvS#7149\nUpdated at')
    for i in range(0, 25):
      try:
        embed.add_field(name = data['districts'][i]['district_name'], value = 'District ID: ' + str(data['districts'][i]['district_id']))
      except IndexError:
        break
    await ctx.channel.send(embed = embed)
  if b:
    embed2 = discord.Embed(title="Districts:", description="Here is a list of available districts", color=0x02fa5d, timestamp = datetime.now(IST))
    embed2.set_author(name = 'We are in this together! Stay Strong!')
    embed2.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')
    embed2.set_footer(text='That is all Folks!\nChoose the corresponding District ID.\nBot made by DhruvS#7149\nUpdated at')
    for i in range(25, 50):
      try:
        embed2.add_field(name = data['districts'][i]['district_name'], value = 'District ID: ' + str(data['districts'][i]['district_id']))
      except IndexError:
        break
    await ctx.channel.send(embed = embed2)
  if c:
    embed3 = discord.Embed(title="Districts:", description="Here is a list of available districts", color=0x02fa5d, timestamp = datetime.now(IST))
    embed3.set_author(name = 'We are in this together! Stay Strong!')
    embed3.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')
    embed3.set_footer(text='That is all Folks!\nChoose the corresponding District ID.\nBot made by DhruvS#7149\nUpdated at')
    for i in range(50, 75):
      try:
        embed3.add_field(name = data['districts'][i]['district_name'], value = 'District ID: ' + str(data['districts'][i]['district_id']))
      except IndexError:
        break
    await ctx.channel.send(embed = embed3)

@bot.command()
async def appointment(ctx, district_id, age = 18, min_avail = 5):
  c = 0
  while c <= 2:
    resp = co.protectedapi(district_id = district_id)
    if resp.status_code == 200:
      break
    else:
      c+=1
  
  while c > 2 & c < 5:
    resp = co.publicapi(district_id = district_id)
    if resp.status_code == 200:
      break
    else:
      c+=1

  data = ap.dataSel(resp, age, min_avail).dataSelection()

  if len(data['centers']) == 0:
    embed1 = discord.Embed(title="Appoinments: ", description="Here is a list of available appoinments", color=0x02fa5d, timestamp = datetime.now(IST))   
    embed1.set_author(name='We are in this together! Stay Strong!')
    embed1.set_thumbnail(url = 'https://cdn.britannica.com/97/1597-004-05816F4E/Flag-India.jpg')
    embed1.set_footer(text='Live data updated at')
    embed1.add_field(name = 'No Avaliable centers :frowning2: ', value = 'Check back later...')
    await ctx.channel.send(embed = embed1)
  
  else:
    for i in range(0, len(data['centers'])):
      pkg = make_app_embed(data['centers'][i], c)
      await ctx.channel.send(embed = pkg)

load_dotenv(find_dotenv())
bot.run(os.getenv("TOKEN"))