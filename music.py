import discord
import yt_dlp

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

async def play(client, message, url):
    if message.author.voice == None:
        await message.channel.send("You need to be in a voice channel to use this command!")
        return

    channel = message.author.voice.channel


    voice_client = discord.utils.get(client.voice_clients, guild=message.guild)

    if voice_client == None:
        voice_client = await channel.connect()
    else:
        await voice_client.move_to(channel)

    with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        playUrl = info['webpage_url']

    source = discord.FFmpegPCMAudio(source=playUrl, **FFMPEG_OPTIONS)
    voice_client.play(source, after=lambda e: print('Song done'))