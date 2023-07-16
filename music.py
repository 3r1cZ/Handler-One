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

vc = None # voice channel
loops = False # looping

# for repeat
timeGlobal = -1 # duration of repeat
index = -1 # song index

# for song lists
with open("musicFiles/musicQuizQuestions.txt") as songs: # list of mp3 file names
    questionList = songs.read().splitlines()
songs.close()
with open("musicFiles/musicQuizAnswers.txt") as answers: # list of anime songs + titles
    answerList = answers.read().splitlines()
# list of anime titles
animeList = []
with open("musicFiles/musicQuizAnswers.txt") as answers:
    for line in answers:
        for i in range(len(line)):
            if line[i] == ' ':
                if line[i+1] == '-':
                    title = line[i+3:-1]
                    animeList.append(title)
answers.close()

# plays a song
async def play(message, time):
    global vc
    global timeGlobal
    global index
    global questionList
    global answerList
    
    if message.guild.voice_client: # if the bot is aready in a voice channel
        if vc.is_playing(): # if a song is already being played
            await message.channel.send("Currently playing song!")
        else: # if a song is not being played, play a song
            randomQuestionNum = randrange(len(questionList))
            index = randomQuestionNum
            player = discord.FFmpegPCMAudio(questionList[randomQuestionNum])
            if time == None:
                vc.play(player, after=lambda e: skip(vc))
                await message.channel.send("Now Playing.")
                print(answerList[randomQuestionNum])
            # if a specific amount of time is specified, play song for that amount of time
            if time != None:
                vc.play(player)
                await message.channel.send("Now Playing.")
                timeGlobal = time
                start = default_timer()
                while default_timer()-start <=int(time):
                    print(default_timer()-start)
                print(answerList[randomQuestionNum])
                vc.pause()
    else:# if the bot is not in a voice channel, it joins it and starts playing
        vc = await message.author.voice.channel.connect() # initializes voice channel
        randomQuestionNum = randrange(len(questionList))
        index = randomQuestionNum
        player = discord.FFmpegPCMAudio(questionList[randomQuestionNum])
        if time == None:
            vc.play(player, after=lambda e: skip(vc))
            await message.channel.send("Now Playing.")
            print(answerList[randomQuestionNum])
        # if a specific amount of time is specified, play song for that amount of time
        if time != None:
            vc.play(player)
            await message.channel.send("Now Playing.")
            timeGlobal = time
            start = default_timer()
            while default_timer()-start <=int(time):
                print(default_timer()-start)
            print(answerList[randomQuestionNum])
            vc.pause()

# repeats a song for a specific duration (timeGlobal)
async def repeat():
    global timeGlobal
    global index
    global vc
    global questionList
    global answerList
    vc.stop()
    player = discord.FFmpegPCMAudio(questionList[index])
    vc.play(player)
    start = default_timer()
    while default_timer()-start <=int(timeGlobal):
        print(default_timer()-start)
    print(answerList[index])
    vc.pause()

# loop a song
def loop(vc, index):
    global questionList
    vc.stop()
    player = discord.FFmpegPCMAudio(questionList[index])
    vc.play(player, after=lambda e: loop(vc, index))

# check for loop
def checkLoop(index):
    global loops
    global vc
    if loops:
        loop(vc, index)

# play a given song
async def playSong(message, index):
    global vc
    global loops
    global questionList
    # user channel
    if message.guild.voice_client: # if the bot is aready in a voice channel
        if vc.is_playing(): # if a song is already being played
            await message.channel.send("Currently playing song!")
        else: # if a song is not being played, play a song
            player = discord.FFmpegPCMAudio(questionList[index])
            vc.play(player, after = lambda e: checkLoop(index))
            await message.channel.send("Now Playing.")
                    
    else:# if the bot is not in a voice channel, it joins it and starts playing
        vc = await message.author.voice.channel.connect()
        player = discord.FFmpegPCMAudio(questionList[index])
        vc.play(player, after = lambda e: checkLoop(index))
        await message.channel.send("Now Playing.")

# skips a song to play a new song
def skip(vc):
    global index
    global questionList
    global answerList
    randomQuestionNum = randrange(len(questionList))
    while randomQuestionNum == index: # ensure song does not repeat
        randomQuestionNum = randrange(len(questionList))
    index = randomQuestionNum
    vc.stop()
    player = discord.FFmpegPCMAudio(questionList[randomQuestionNum])
    vc.play(player, after=lambda e: skip(vc))
    print(answerList[randomQuestionNum])

# pauses a song
def pause(vc):
    vc.pause()

# resumes a song
def resume(vc):
    vc.resume()

# bot leaves the voice channel it is currently in
async def leave(message):
    global loops
    if message.guild.voice_client: # If the bot is in a voice channel 
        await message.guild.voice_client.disconnect() # Leave the channel
        await message.channel.send('Left the voice channel!')
        # resetting everything
        loops = False
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

## quick sorting

# Function to find the partition position
def partition(array, low, high):
    global questionList
    global answerList
    global animeList
 
    # choose the rightmost element as pivot
    pivot = array[high]
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
            if array != answerList:
                (answerList[i], answerList[j]) = (answerList[j], answerList[i])
            if array != animeList:
                (animeList[i], animeList[j]) = (animeList[j], animeList[i])
            (questionList[i], questionList[j]) = (questionList[j], questionList[i])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    if array != answerList:
        (answerList[i + 1], answerList[high]) = (answerList[high], answerList[i + 1])
    if array != animeList:
        (animeList[i + 1], animeList[high]) = (animeList[high], animeList[i + 1])    
    (questionList[i+1], questionList[high]) = (questionList[high], questionList[i+1])
 
    # Return the position from where partition is done
    return i + 1
 
# function to perform quicksort
def quickSort(array, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)
 
        # Recursive call on the left of pivot
        quickSort(array, low, pi - 1)
 
        # Recursive call on the right of pivot
        quickSort(array, pi + 1, high)
 
