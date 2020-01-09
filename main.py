import os, requests, youtube_dl, discord, asyncio
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.tasks import loop

token = 'NjY0MDg2NTY0MDUzMzE5NzAw.XhcNqQ.XvILEyYiHKdqg6QTAraau2LXtx0'

client = commands.Bot(command_prefix='/')

options = {
  'format': 'bestaudio/best',
  'extractaudio' : True,  # only keep the audio
  'audioformat' : "mp3",  # convert to mp3
  'outtmpl': 'temp.mp3',    # name the file the ID of the video
  'noplaylist' : True,    # only download single song, not playlist
}

rgbw = [
  {'r' : 255, 'g' : 0, 'b' : 0},
  {'r' : 255, 'g' : 128, 'b' : 0},
  {'r' : 255, 'g' : 255, 'b' : 0},
  {'r' : 128, 'g' : 255, 'b' : 0},
  {'r' : 0, 'g' : 255, 'b' : 255},
  {'r' : 0, 'g' : 0, 'b' : 255},
  {'r' : 127, 'g' : 0, 'b' : 255},
  {'r' : 255, 'g' : 0, 'b' : 255},
  {'r' : 255, 'g' : 0, 'b' : 127},
  {'r' : 255, 'g' : 0, 'b' : 77},
]

roles = []

def query_url(query):
    query = query.replace(' ', '+')
    url = 'https://www.youtube.com/results?search_query={}'.format(query)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return 'https://www.youtube.com{}'.format(soup.find_all('a', class_='yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link')[0]['href'])

@client.event
async def on_ready():
  print('BOT ONLINE')

@loop()
async def rainbow():
      for rgb in rgbw:
        for role in roles:
          await role.edit(colour=discord.Colour.from_rgb(rgb['r'], rgb['g'], rgb['b']))

@client.command(pass_context=True)
async def rme(ctx):
  roles.append(ctx.message.author.roles[-1])
  print('Rainbow Users:\n')
  print(roles)

@client.command(pass_context=True)
async def logo(ctx):
    channel = ctx.message.channel
    logo = discord.File('Adsomnia.png')
    await channel.send(file=logo)

rainbow.start()
client.run(token)