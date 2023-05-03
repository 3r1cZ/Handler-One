import discord
import asyncio
import youtube_dl
import urllib.request
import re
import pafy
import yt_dlp

voice_clients = {}

yt_dl_opts = {'default_search': 'auto'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

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

async def play(client, message, url):
    if message.author.voice == None:
        await message.channel.send("You need to be in a voice channel to use this command!")
        return

    channel = message.author.voice.channel

    voice = discord.utils.get(message.guild.voice_channels, name=channel.name)

    voice_client = discord.utils.get(client.voice_clients, guild=message.guild)

    if voice_client == None:
        voice_client = await voice.connect()
    else:
        await voice_client.move_to(channel)

    with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        playUrl = info["url"]
        print(playUrl)

    source = discord.FFmpegPCMAudio(playUrl, options=ffmpeg_options)
    voice.play(source)
    # search = search.replace(" ", "+")

    # html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
    # video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        
    # # await message.channel.send("https://www.youtube.com/watch?v=" + video_ids[0])

    # song = pafy.new(video_ids[0])  # creates a new pafy object

    # audio = song.getbestaudio()  # gets an audio source

    # source = discord.FFmpegPCMAudio(audio.url, **ffmpeg_options)  # converts the youtube audio source into a source discord can use

    # voice_client.play(source)  # play the source