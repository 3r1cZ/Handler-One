import discord
import asyncio
import youtube_dl

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

async def play(message, song):
    try:
        voice_client = await message.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except:
        await message.channel.send('Please join a voice channel!')
        print("error")

    try:
        url = message.content.split()[1]

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        song = data['url']
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

        voice_clients[message.guild.id].play(player)

    except Exception as err:
        print(err)