import os, requests, youtube_dl, discord
from bs4 import BeautifulSoup
from discord.ext import commands

token = 'NjY0MDg2NTY0MDUzMzE5NzAw.XhR-jQ.dJQNv62KTGHA5pKxR-c6tP8S_Hk'

client = commands.Bot(command_prefix='/')

options = {
  'format': 'bestaudio/best',
  'extractaudio' : True,  # only keep the audio
  'audioformat' : "mp3",  # convert to mp3
  'outtmpl': 'temp.mp3',    # name the file the ID of the video
  'noplaylist' : True,    # only download single song, not playlist
}


def query_url(query):
    query = query.replace(' ', '+')
    url = 'https://www.youtube.com/results?search_query={}'.format(query)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return 'https://www.youtube.com{}'.format(soup.find_all('a', class_='yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link')[0]['href'])

@client.event
async def on_ready():
    print('Bot online.')

@client.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, query):
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([query_url(query)])
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('temp.mp3'))
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 1

@client.command(pass_context=True)
async def rme(ctx):
    ctx.message.author.roles[-1].edit(discord.Colour.from_rgb(255, 0, 0))

@client.command(pass_context=True)
async def logo(ctx):
    channel = ctx.message.channel
    logo = discord.File('Adsomnia.png')
    await channel.send(file=logo)
client.run(token)