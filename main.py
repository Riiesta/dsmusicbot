import discord
from discord.ext import commands
import yt_dlp as youtube_dl # Используем yt-dlp вместо youtube_dl

from config import TOKEN

# Включите все необходимые намерения
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True  # Это новое намерение для доступа к содержанию сообщений

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return

    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',  # IPv4
        'verbose': True  # Включение подробного логирования
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            audio_url = next((format['url'] for format in info['formats'] if format['acodec'] != 'none'), None)
            if not audio_url:
                await ctx.send("Could not retrieve audio from the provided URL.")
                return
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')
            return

        voice_client.play(discord.FFmpegPCMAudio(audio_url, executable='C:/Ffmpeg/ffmpeg-2023-11-05-git-44a0148fad-full_build/ffmpeg-2023-11-05-git-44a0148fad-full_build/bin/ffmpeg.exe'), after=lambda e: print(f'Player error: {e}') if e else None)

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

bot.run(TOKEN)
