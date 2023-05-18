import discord
import yt_dlp
import asyncio
from random import randrange

FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
            }

YTDLP_OPTIONS = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch',
                'source_address': '0.0.0.0',
}

vc = None

async def play(message):
    global vc
    with open("musicQuizQuestions.txt") as songs:
        songList = songs.read().splitlines()
    # grab the user who sent the command
    voice_channel=message.author.voice
    # only play music if user is in a voice channel
    if voice_channel!= None:
        print(message.guild.voice_client)
        if message.guild.voice_client:
            if vc.is_playing():
                await message.channel.send("Currently playing song!")
            else:
                randomQuestionNum = randrange(len(songList))
                player = discord.FFmpegPCMAudio(songList[randomQuestionNum])
                vc.play(player, after=lambda e: skip(vc))
                await message.channel.send("Now Playing.")
        else:# create StreamPlayer
            vc = await voice_channel.channel.connect()
            randomQuestionNum = randrange(len(songList))
            player = discord.FFmpegPCMAudio(songList[randomQuestionNum])
            vc.play(player, after=lambda e: skip(vc))
            await message.channel.send("Now Playing.")
    else:
        await message.channel.send('Must be in a channel!')
    songs.close()

def skip(vc):
    with open("musicQuizQuestions.txt") as songs:
        songList = songs.read().splitlines()
    randomQuestionNum = randrange(len(songList))
    vc.stop()
    player = discord.FFmpegPCMAudio(songList[randomQuestionNum])
    vc.play(player, after=lambda e: skip(vc))

def pause(vc):
    vc.pause()

def resume(vc):
    vc.resume()

async def leave(message):
    if message.guild.voice_client: # If the bot is in a voice channel 
        await message.guild.voice_client.disconnect() # Leave the channel
        await message.channel.send('Left the voice channel!')
    else: 
        await message.channel.send("Currently not in a voice channel!")
    # if message.author.voice == None:
    #     await message.channel.send("You need to be in a voice channel to use this command!")
    #     return

    # channel = message.author.voice.channel


    # voice_client = discord.utils.get(client.voice_clients, guild=message.guild)

    # if voice_client == None:
    #     voice_client = await channel.connect()
    # else:
    #     await voice_client.move_to(channel)

    # with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
    #     info = ydl.extract_info(url, download=False)
    #     playUrl = info['webpage_url']

    # source = discord.FFmpegPCMAudio(source=playUrl, **FFMPEG_OPTIONS)
    # voice_client.play(source, after=lambda e: print('Song done'))