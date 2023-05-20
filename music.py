# This class implements the music features of the discord bot

import discord
import yt_dlp
from random import randrange
from timeit import default_timer

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

# plays a song
async def play(message, time):
    global vc
    with open("musicFiles/musicQuizQuestions.txt") as songs:
        songList = songs.read().splitlines()
    with open("musicFiles/musicQuizAnswers.txt") as answers:
        answerList = answers.read().splitlines()
    # user channel
    voice_channel=message.author.voice
    # only play music if user is in a voice channel
    if voice_channel!= None:
        if message.guild.voice_client: # if the bot is aready in a voice channel
            if vc.is_playing(): # if a song is already being played
                await message.channel.send("Currently playing song!")
            else: # if a song is not being played, play a song
                randomQuestionNum = randrange(len(songList))
                player = discord.FFmpegPCMAudio(songList[randomQuestionNum])
                vc.play(player, after=lambda e: skip(vc))
                await message.channel.send("Now Playing.")
                # if a specific amount of time is specified, play song for that amount of time
                if time != None:
                    start = default_timer()
                    while default_timer()-start <=int(time):
                        print(default_timer()-start)
                    print(answerList[randomQuestionNum])
                    vc.pause()
        else:# if the bot is not in a voice channel, it joins it and starts playing
            vc = await voice_channel.channel.connect()
            randomQuestionNum = randrange(len(songList))
            player = discord.FFmpegPCMAudio(songList[randomQuestionNum])
            vc.play(player, after=lambda e: skip(vc))
            await message.channel.send("Now Playing.")
            # if a specific amount of time is specified, play song for that amount of time
            if time != None:
                start = default_timer()
                while default_timer()-start <=int(time):
                    print(default_timer()-start)
                print(answerList[randomQuestionNum])
                vc.pause()
    else:
        await message.channel.send('Must be in a channel!')
    songs.close()
    answers.close()

# play a given song
async def playSong(message, index):
    global vc
    with open("musicFiles/musicQuizQuestions.txt") as songs:
        songList = songs.read().splitlines()
    # user channel
    voice_channel=message.author.voice
    # only play music if user is in a voice channel
    if voice_channel!= None:
        if message.guild.voice_client: # if the bot is aready in a voice channel
            if vc.is_playing(): # if a song is already being played
                await message.channel.send("Currently playing song!")
            else: # if a song is not being played, play a song
                player = discord.FFmpegPCMAudio(songList[index])
                vc.play(player)
                await message.channel.send("Now Playing.")
                        
        else:# if the bot is not in a voice channel, it joins it and starts playing
            vc = await voice_channel.channel.connect()
            player = discord.FFmpegPCMAudio(songList[index])
            vc.play(player)
            await message.channel.send("Now Playing.")
    else:
        await message.channel.send('Must be in a channel!')
    songs.close()

# skips a song to play a new song
def skip(vc):
    with open("musicFiles/musicQuizQuestions.txt") as songs:
        songList = songs.read().splitlines()
    with open("musicFiles/musicQuizAnswers.txt") as answers:
        answerList = answers.read().splitlines()
    randomQuestionNum = randrange(len(songList))
    vc.stop()
    player = discord.FFmpegPCMAudio(songList[randomQuestionNum])
    print(answerList[randomQuestionNum])
    vc.play(player, after=lambda e: skip(vc))
    songs.close()
    answers.close()

# pauses a song
def pause(vc):
    vc.pause()

# resumes a song
def resume(vc):
    vc.resume()

# bot leaves the voice channel it is currently in
async def leave(message):
    if message.guild.voice_client: # If the bot is in a voice channel 
        await message.guild.voice_client.disconnect() # Leave the channel
        await message.channel.send('Left the voice channel!')
    else: 
        await message.channel.send("Currently not in a voice channel!")

# plays a YouTube URL
async def playYoutube(client, message, url):
    if message.author.voice == None: # checks if a user is in a voice channel
        await message.channel.send("You need to be in a voice channel to use this command!")
        return

    channel = message.author.voice.channel

    voice_client = discord.utils.get(client.voice_clients, guild=message.guild)

    # checks if the bot is already in a channel
    if voice_client == None:
        voice_client = await channel.connect()
    else:
        await voice_client.move_to(channel)

    # obtains a playable source from a given URL
    with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        playUrl = info['entries'][0]['webpage_url']
        # playUrl = info['webpage_url']
    print(playUrl)
    source = discord.FFmpegPCMAudio(playUrl, **FFMPEG_OPTIONS)
    voice_client.play(source, after=lambda e: print('Song done'))