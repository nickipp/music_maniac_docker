import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
import urlcheck

def run_bot():
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix=".", intents=intents)

    queues = {}
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

    @client.event
    async def on_ready():
        print(f'{client.user} is now jamming')

    async def play(ctx, *, link):
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        try:
            print(link)
            link = await urlcheck.clean_url(await urlcheck.yourl(link))
            print(link)
            if link == "invalid":
                ctx.send("Invalid URL")
                asyncio.run_coroutine_threadsafe(play_next(ctx),client.loop)

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))

        except Exception as e:
            print(e)

    async def play_next(ctx):
        if ctx.guild.id in queues:
            if queues[ctx.guild.id] == []:
                del queues[ctx.guild.id]
                await asyncio.run_coroutine_threadsafe(stop(ctx), client.loop)
            link = queues[ctx.guild.id].pop(0)
            await play(ctx, link=link)
        if ctx.guild.id not in queues:
            await asyncio.run_coroutine_threadsafe(stop(ctx), client.loop)

    @client.command(name="clear_queue")
    async def clear_queue(ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()
            await ctx.send("Queue cleared!")
        else:
            await ctx.send("There is no queue to clear")

    @client.command(name="stop")
    async def stop(ctx):
        try:
            await clear_queue(ctx)
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    @client.command(name="skip")
    async def skip(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
        except Exception as e:
            print(e)

    @client.command(name="play")
    async def queue(ctx, *, url):
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
            queues[ctx.guild.id].append(url)
            await play_next(ctx)
        else:
            queues[ctx.guild.id].append(url)
            await ctx.send("Added to queue!")

    client.run(TOKEN)
