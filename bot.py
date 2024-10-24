import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content events

bot = commands.Bot(command_prefix="!", intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True
}

async def play_audio(ctx, url):
    try:
        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await voice_channel.connect()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2)
            ctx.voice_client.play(source, after=lambda e: print(f"Finished playing: {e}"))

        await ctx.send(f"Now playing: {info['title']}")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command()
async def play(ctx, url: str):
    await play_audio(ctx, url)

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

bot.run(os.getenv('MTI5ODczNzE0ODY5ODE2NTMyMA.GIieeX.w3CTW64G3jjQWnaiBnn8HQVwE6x_2ntAfantS8'))

